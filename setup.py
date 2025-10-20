"""Setup script for YouTube Automation System"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg installed")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("❌ FFmpeg not found")
    print("   Install from: https://ffmpeg.org/download.html")
    return False


def create_directories():
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
    
    print("✅ Directories created")
    return True


def create_env_file():
    """Create .env file if not exists"""
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✅ .env file created (please edit with your API keys)")
        return True
    else:
        print("✅ .env file exists")
        return True


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def check_credentials():
    """Check for YouTube credentials"""
    if os.path.exists('client_secret.json'):
        print("✅ client_secret.json found")
        return True
    else:
        print("⚠️  client_secret.json not found")
        print("   Download from Google Cloud Console for YouTube upload")
        return False


def main():
    """Run setup"""
    print("=" * 60)
    print("🎬 YOUTUBE AUTOMATION - SETUP")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version()),
        ("FFmpeg", check_ffmpeg()),
        ("Directories", create_directories()),
        ("Environment File", create_env_file()),
    ]
    
    print("\n📦 Installing dependencies...")
    checks.append(("Dependencies", install_dependencies()))
    
    print("\n🔑 Checking credentials...")
    checks.append(("YouTube Credentials", check_credentials()))
    
    print("\n" + "=" * 60)
    print("SETUP SUMMARY")
    print("=" * 60)
    
    for name, status in checks:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {name}")
    
    all_passed = all(status for _, status in checks)
    
    if all_passed:
        print("\n✅ Setup complete! Ready to generate videos.")
        print("\n🚀 Quick start:")
        print("   python main.py --mode single --no-upload")
    else:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")
        
        if not checks[1][1]:  # FFmpeg
            print("\n📝 To install FFmpeg:")
            print("   Windows: Download from https://ffmpeg.org/download.html")
            print("   Linux: sudo apt install ffmpeg")
            print("   macOS: brew install ffmpeg")
        
        if not checks[5][1]:  # Credentials
            print("\n📝 To get YouTube credentials:")
            print("   1. Go to https://console.cloud.google.com/")
            print("   2. Create project and enable YouTube Data API v3")
            print("   3. Create OAuth 2.0 credentials")
            print("   4. Download as client_secret.json")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
