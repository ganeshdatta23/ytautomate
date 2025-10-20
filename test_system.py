"""Test script to verify all components work"""
import os
import sys
import yaml
from colorama import init, Fore

init(autoreset=True)


def test_imports():
    """Test all imports"""
    print(f"{Fore.YELLOW}Testing imports...")
    try:
        from src.script_generator import ScriptGenerator
        from src.voice_generator import VoiceGenerator
        from src.image_generator import ImageGenerator
        from src.video_assembler import VideoAssembler
        from src.thumbnail_creator import ThumbnailCreator
        from src.uploader import YouTubeUploader
        print(f"{Fore.GREEN}✅ All imports successful")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Import failed: {e}")
        return False


def test_config():
    """Test configuration loading"""
    print(f"\n{Fore.YELLOW}Testing configuration...")
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        with open('config/prompts.yaml', 'r') as f:
            prompts = yaml.safe_load(f)
        print(f"{Fore.GREEN}✅ Configuration loaded")
        print(f"   Niche: {config['content']['niche']}")
        print(f"   Voice: {config['voice']['voice_name']}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Config failed: {e}")
        return False


def test_directories():
    """Test directory structure"""
    print(f"\n{Fore.YELLOW}Testing directories...")
    dirs = [
        'data/scripts',
        'data/audio',
        'data/images',
        'data/videos',
        'data/thumbnails',
        'logs'
    ]
    
    all_exist = True
    for d in dirs:
        if os.path.exists(d):
            print(f"{Fore.GREEN}✅ {d}")
        else:
            print(f"{Fore.RED}❌ {d} missing")
            all_exist = False
    
    return all_exist


def test_script_generation():
    """Test script generation"""
    print(f"\n{Fore.YELLOW}Testing script generation...")
    try:
        from src.script_generator import ScriptGenerator
        
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        with open('config/prompts.yaml', 'r') as f:
            prompts = yaml.safe_load(f)
        
        generator = ScriptGenerator(config, prompts)
        metadata = generator.generate()
        
        print(f"{Fore.GREEN}✅ Script generated")
        print(f"   Title: {metadata['title'][:50]}...")
        print(f"   Words: {metadata['word_count']}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Script generation failed: {e}")
        return False


def test_voice_generation():
    """Test voice generation"""
    print(f"\n{Fore.YELLOW}Testing voice generation...")
    try:
        from src.voice_generator import VoiceGenerator
        
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        generator = VoiceGenerator(config)
        test_text = "This is a test of the voice generation system."
        output_path = 'data/audio/test_voice.mp3'
        
        success = generator.generate(test_text, output_path)
        
        if success and os.path.exists(output_path):
            duration = generator.get_audio_duration(output_path)
            print(f"{Fore.GREEN}✅ Voice generated")
            print(f"   Duration: {duration:.2f}s")
            print(f"   File: {output_path}")
            os.remove(output_path)
            return True
        else:
            print(f"{Fore.RED}❌ Voice generation failed")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Voice generation failed: {e}")
        return False


def test_ffmpeg():
    """Test FFmpeg availability"""
    print(f"\n{Fore.YELLOW}Testing FFmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"{Fore.GREEN}✅ FFmpeg available")
            print(f"   {version}")
            return True
    except Exception as e:
        print(f"{Fore.RED}❌ FFmpeg not found: {e}")
        print(f"   Install from: https://ffmpeg.org/download.html")
        return False


def main():
    """Run all tests"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🧪 YOUTUBE AUTOMATION - SYSTEM TEST")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    tests = [
        ("Imports", test_imports()),
        ("Configuration", test_config()),
        ("Directories", test_directories()),
        ("FFmpeg", test_ffmpeg()),
        ("Script Generation", test_script_generation()),
        ("Voice Generation", test_voice_generation()),
    ]
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}TEST SUMMARY")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        symbol = f"{Fore.GREEN}✅" if result else f"{Fore.RED}❌"
        print(f"{symbol} {name}")
    
    print(f"\n{Fore.CYAN}{'='*60}")
    
    if passed == total:
        print(f"{Fore.GREEN}✅ ALL TESTS PASSED ({passed}/{total})")
        print(f"\n{Fore.GREEN}🚀 System ready! Run:")
        print(f"{Fore.YELLOW}   python main.py --mode single --no-upload")
    else:
        print(f"{Fore.YELLOW}⚠️  TESTS PASSED: {passed}/{total}")
        print(f"\n{Fore.YELLOW}Fix the failed tests before running main.py")
    
    print(f"{Fore.CYAN}{'='*60}\n")


if __name__ == '__main__':
    main()
