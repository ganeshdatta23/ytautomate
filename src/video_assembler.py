"""Video Assembler - Creates videos with effects using FFmpeg and MoviePy"""
import os
import logging
import subprocess
from typing import List
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, 
    concatenate_videoclips, VideoFileClip
)
from PIL import Image
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoAssembler:
    def __init__(self, config: dict):
        self.config = config
        self.resolution = tuple(map(int, config['video']['resolution'].split('x')))
        self.fps = config['video']['fps']
        self.codec = config['video']['codec']
        self.bitrate = config['video']['bitrate']
        self.transition_duration = config['images']['transition_duration']
        self.ken_burns = config['images']['ken_burns']
    
    def assemble(self, image_paths: List[str], audio_path: str, output_path: str) -> bool:
        """Assemble video from images and audio"""
        try:
            logger.info("🎬 Assembling video...")
            
            audio = AudioFileClip(audio_path)
            audio_duration = audio.duration
            
            logger.info(f"⏱️ Audio duration: {audio_duration:.2f}s")
            logger.info(f"🖼️ Images: {len(image_paths)}")
            
            clips = self._create_image_clips(image_paths, audio_duration)
            
            logger.info("🎞️ Concatenating clips...")
            video = concatenate_videoclips(clips, method="compose")
            
            logger.info("🔊 Adding audio...")
            video = video.set_audio(audio)
            
            logger.info("💾 Rendering video...")
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec=self.codec,
                bitrate=self.bitrate,
                audio_codec='aac',
                threads=4,
                preset='medium',
                logger=None
            )
            
            video.close()
            audio.close()
            
            logger.info(f"✅ Video assembled: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Video assembly failed: {e}")
            raise
    
    def _create_image_clips(self, image_paths: List[str], total_duration: float) -> List[ImageClip]:
        """Create image clips with effects"""
        clips = []
        
        duration_per_image = total_duration / len(image_paths)
        
        for i, img_path in enumerate(image_paths):
            logger.info(f"Processing image {i+1}/{len(image_paths)}")
            
            clip = ImageClip(img_path, duration=duration_per_image)
            
            clip = clip.resize(self.resolution)
            
            if self.ken_burns:
                clip = self._apply_ken_burns(clip)
            
            if i < len(image_paths) - 1:
                clip = clip.crossfadeout(self.transition_duration)
            
            clips.append(clip)
        
        return clips
    
    def _apply_ken_burns(self, clip: ImageClip) -> ImageClip:
        """Apply Ken Burns effect (zoom/pan)"""
        effect_type = random.choice(['zoom_in', 'zoom_out', 'pan_right', 'pan_left'])
        
        duration = clip.duration
        w, h = self.resolution
        
        if effect_type == 'zoom_in':
            def zoom_in_effect(get_frame, t):
                frame = get_frame(t)
                zoom = 1 + (t / duration) * 0.1
                return self._zoom_frame(frame, zoom)
            
            return clip.fl(zoom_in_effect)
        
        elif effect_type == 'zoom_out':
            def zoom_out_effect(get_frame, t):
                frame = get_frame(t)
                zoom = 1.1 - (t / duration) * 0.1
                return self._zoom_frame(frame, zoom)
            
            return clip.fl(zoom_out_effect)
        
        elif effect_type == 'pan_right':
            def pan_right_effect(get_frame, t):
                frame = get_frame(t)
                shift = int((t / duration) * w * 0.05)
                return self._shift_frame(frame, shift, 0)
            
            return clip.fl(pan_right_effect)
        
        elif effect_type == 'pan_left':
            def pan_left_effect(get_frame, t):
                frame = get_frame(t)
                shift = -int((t / duration) * w * 0.05)
                return self._shift_frame(frame, shift, 0)
            
            return clip.fl(pan_left_effect)
        
        return clip
    
    def _zoom_frame(self, frame, zoom):
        """Zoom frame"""
        import numpy as np
        from scipy.ndimage import zoom as scipy_zoom
        
        h, w = frame.shape[:2]
        
        zoomed = scipy_zoom(frame, (zoom, zoom, 1), order=1)
        
        zh, zw = zoomed.shape[:2]
        
        y1 = (zh - h) // 2
        x1 = (zw - w) // 2
        
        if y1 < 0 or x1 < 0:
            result = np.zeros_like(frame)
            y_offset = max(0, -y1)
            x_offset = max(0, -x1)
            y1 = max(0, y1)
            x1 = max(0, x1)
            
            crop_h = min(zh, h - y_offset)
            crop_w = min(zw, w - x_offset)
            
            result[y_offset:y_offset+crop_h, x_offset:x_offset+crop_w] = zoomed[y1:y1+crop_h, x1:x1+crop_w]
            return result
        
        return zoomed[y1:y1+h, x1:x1+w]
    
    def _shift_frame(self, frame, shift_x, shift_y):
        """Shift frame"""
        import numpy as np
        
        h, w = frame.shape[:2]
        result = np.zeros_like(frame)
        
        src_x1 = max(0, -shift_x)
        src_x2 = min(w, w - shift_x)
        src_y1 = max(0, -shift_y)
        src_y2 = min(h, h - shift_y)
        
        dst_x1 = max(0, shift_x)
        dst_x2 = dst_x1 + (src_x2 - src_x1)
        dst_y1 = max(0, shift_y)
        dst_y2 = dst_y1 + (src_y2 - src_y1)
        
        result[dst_y1:dst_y2, dst_x1:dst_x2] = frame[src_y1:src_y2, src_x1:src_x2]
        
        return result
    
    def add_background_music(self, video_path: str, music_path: str, output_path: str) -> bool:
        """Add background music to video"""
        try:
            if not os.path.exists(music_path):
                logger.warning("No background music found, skipping")
                return False
            
            logger.info("🎵 Adding background music...")
            
            video = VideoFileClip(video_path)
            music = AudioFileClip(music_path)
            
            if music.duration < video.duration:
                loops = int(video.duration / music.duration) + 1
                music = concatenate_videoclips([music] * loops)
            
            music = music.subclip(0, video.duration)
            
            music_volume = self.config['video'].get('background_music_volume', 0.2)
            music = music.volumex(music_volume)
            
            from moviepy.audio.AudioClip import CompositeAudioClip
            final_audio = CompositeAudioClip([video.audio, music])
            
            final_video = video.set_audio(final_audio)
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec=self.codec,
                bitrate=self.bitrate,
                audio_codec='aac',
                threads=4,
                preset='medium',
                logger=None
            )
            
            final_video.close()
            video.close()
            music.close()
            
            logger.info(f"✅ Background music added: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Background music error: {e}")
            return False


def main():
    """Test video assembler"""
    import yaml
    
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    assembler = VideoAssembler(config)
    
    print("Video assembler initialized")
    print(f"Resolution: {assembler.resolution}")
    print(f"FPS: {assembler.fps}")
    print(f"Ken Burns: {assembler.ken_burns}")


if __name__ == '__main__':
    main()
