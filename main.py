"""Main YouTube Automation System - Production Ready"""
import os
import sys
import argparse
import logging
import yaml
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from colorama import init, Fore, Style

from src.script_generator import ScriptGenerator
from src.voice_generator import VoiceGenerator
from src.image_generator import ImageGenerator
from src.video_assembler import VideoAssembler
from src.thumbnail_creator import ThumbnailCreator
from src.uploader import YouTubeUploader

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class YouTubeAutomation:
    def __init__(self, config_path: str = 'config/config.yaml', prompts_path: str = 'config/prompts.yaml'):
        load_dotenv()
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        with open(prompts_path, 'r') as f:
            self.prompts = yaml.safe_load(f)
        
        self.script_gen = ScriptGenerator(self.config, self.prompts)
        self.voice_gen = VoiceGenerator(self.config)
        self.image_gen = ImageGenerator(self.config)
        self.video_asm = VideoAssembler(self.config)
        self.thumb_creator = ThumbnailCreator(self.config)
        self.uploader = YouTubeUploader(self.config)
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        dirs = [
            'data/scripts',
            'data/audio',
            'data/images',
            'data/videos',
            'data/thumbnails',
            'logs'
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def generate_single_video(self, niche: str = None, upload: bool = True) -> dict:
        """Generate a single video"""
        try:
            if niche:
                self.config['content']['niche'] = niche
                self.script_gen.niche = niche
            
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.CYAN}YOUTUBE AUTOMATION - STARTING")
            print(f"{Fore.CYAN}{'='*60}\n")
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_id = f"{self.config['content']['niche']}_{timestamp}"
            
            print(f"{Fore.YELLOW}Step 1/6: Generating script...")
            metadata = self.script_gen.generate()
            script_path = self.script_gen.save(metadata, 'data/scripts')
            print(f"{Fore.GREEN}[OK] Script: {metadata['title']}")
            print(f"{Fore.GREEN}   Words: {metadata['word_count']}")
            
            print(f"\n{Fore.YELLOW}Step 2/6: Generating voiceover...")
            audio_path = f"data/audio/{video_id}.mp3"
            self.voice_gen.generate(metadata['script'], audio_path)
            audio_duration = self.voice_gen.get_audio_duration(audio_path)
            print(f"{Fore.GREEN}[OK] Audio: {audio_duration:.2f} seconds")
            
            print(f"\n{Fore.YELLOW}Step 3/6: Generating images...")
            image_dir = f"data/images/{video_id}"
            image_paths = self.image_gen.generate_for_script(metadata['script'], image_dir)
            print(f"{Fore.GREEN}[OK] Images: {len(image_paths)} generated")
            
            print(f"\n{Fore.YELLOW}Step 4/6: Assembling video...")
            video_path = f"data/videos/{video_id}.mp4"
            self.video_asm.assemble(image_paths, audio_path, video_path)
            print(f"{Fore.GREEN}[OK] Video: {video_path}")
            
            print(f"\n{Fore.YELLOW}Step 5/6: Creating thumbnail...")
            thumbnail_path = f"data/thumbnails/{video_id}.jpg"
            self.thumb_creator.create(image_paths[0], metadata['title'], thumbnail_path)
            print(f"{Fore.GREEN}[OK] Thumbnail: {thumbnail_path}")
            
            result = {
                'video_id': video_id,
                'title': metadata['title'],
                'video_path': video_path,
                'thumbnail_path': thumbnail_path,
                'metadata': metadata,
                'timestamp': timestamp
            }
            
            if upload:
                print(f"\n{Fore.YELLOW}Step 6/6: Uploading to YouTube...")
                yt_video_id = self.uploader.upload(video_path, metadata, thumbnail_path)
                
                if yt_video_id:
                    result['youtube_id'] = yt_video_id
                    result['youtube_url'] = f"https://www.youtube.com/watch?v={yt_video_id}"
                    print(f"{Fore.GREEN}[OK] Uploaded: {result['youtube_url']}")
                else:
                    print(f"{Fore.RED}[ERROR] Upload failed")
            else:
                print(f"\n{Fore.BLUE}Step 6/6: Skipped (--no-upload flag)")
            
            self._save_result(result)
            
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.GREEN}VIDEO GENERATION COMPLETE!")
            print(f"{Fore.CYAN}{'='*60}\n")
            
            return result
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            print(f"\n{Fore.RED}[ERROR]: {e}")
            raise
    
    def generate_batch(self, count: int, niche: str = None, upload: bool = True) -> list:
        """Generate multiple videos"""
        results = []
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}BATCH MODE: Generating {count} videos")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        for i in range(count):
            print(f"\n{Fore.MAGENTA}{'='*60}")
            print(f"{Fore.MAGENTA}VIDEO {i+1}/{count}")
            print(f"{Fore.MAGENTA}{'='*60}")
            
            try:
                result = self.generate_single_video(niche, upload)
                results.append(result)
            except Exception as e:
                logger.error(f"Video {i+1} failed: {e}")
                print(f"{Fore.RED}[ERROR] Video {i+1} failed, continuing...")
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}BATCH COMPLETE: {len(results)}/{count} successful")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        return results
    
    def _save_result(self, result: dict):
        """Save result to JSON log"""
        log_file = 'logs/videos.json'
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(result)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='YouTube Automation System')
    
    parser.add_argument('--mode', choices=['single', 'batch', 'schedule'], default='single',
                       help='Operation mode')
    parser.add_argument('--niche', choices=['psychology_facts', 'history_mystery', 'finance', 'reddit_stories'],
                       help='Content niche')
    parser.add_argument('--count', type=int, default=1,
                       help='Number of videos (batch mode)')
    parser.add_argument('--no-upload', action='store_true',
                       help='Skip YouTube upload')
    parser.add_argument('--privacy', choices=['public', 'private', 'unlisted'], default='public',
                       help='Video privacy setting')
    
    args = parser.parse_args()
    
    try:
        automation = YouTubeAutomation()
        
        if args.privacy:
            automation.config['youtube']['privacy'] = args.privacy
        
        upload = not args.no_upload
        
        if args.mode == 'single':
            automation.generate_single_video(args.niche, upload)
        
        elif args.mode == 'batch':
            automation.generate_batch(args.count, args.niche, upload)
        
        elif args.mode == 'schedule':
            print(f"{Fore.YELLOW}Schedule mode not yet implemented")
            print(f"{Fore.BLUE}Use cron (Linux/Mac) or Task Scheduler (Windows) to run:")
            print(f"   python main.py --mode single --niche {args.niche or 'psychology_facts'}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[WARNING] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
