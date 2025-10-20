# 📦 Installation Guide

Complete installation instructions for all platforms.

## 🖥️ System Requirements

- **OS**: Windows 10+, Ubuntu 20.04+, macOS 10.15+
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk**: 10 GB free space
- **Internet**: Required for image download and upload

## 📋 Prerequisites

### 1. Python Installation

#### Windows
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Verify: `python --version`

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

#### macOS
```bash
# Using Homebrew
brew install python3
python3 --version
```

### 2. FFmpeg Installation (Required)

#### Windows

**Method 1: Direct Download**
1. Go to https://ffmpeg.org/download.html
2. Download Windows build (gyan.dev recommended)
3. Extract to `C:\ffmpeg`
4. Add to PATH:
   - Open System Properties → Environment Variables
   - Edit "Path" variable
   - Add `C:\ffmpeg\bin`
   - Click OK
5. Restart terminal
6. Verify: `ffmpeg -version`

**Method 2: Chocolatey**
```bash
choco install ffmpeg
```

**Method 3: Scoop**
```bash
scoop install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg
ffmpeg -version
```

### 3. Git (Optional)

#### Windows
Download from https://git-scm.com/download/win

#### Linux
```bash
sudo apt install git
```

#### macOS
```bash
brew install git
```

## 🚀 Project Installation

### Method 1: Download ZIP

1. Download project ZIP
2. Extract to desired location
3. Open terminal in project folder

### Method 2: Git Clone

```bash
git clone <repository-url>
cd youtube-automation
```

## 🔧 Setup Steps

### Step 1: Create Virtual Environment

#### Windows
```bash
cd youtube-automation
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS
```bash
cd youtube-automation
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 2: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- edge-tts (voice generation)
- gtts (fallback voice)
- pyttsx3 (offline voice)
- moviepy (video editing)
- Pillow (image processing)
- google-api-python-client (YouTube)
- And more...

**Installation time: 2-5 minutes**

### Step 3: Configure Environment

```bash
# Copy example file
cp .env.example .env

# Windows
copy .env.example .env
```

Edit `.env` file:

```env
# Required for YouTube upload
YOUTUBE_CLIENT_ID=your-client-id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your-client-secret

# Optional: Better images (free)
PEXELS_API_KEY=your-pexels-api-key

# Optional: AI scripts (free)
HUGGINGFACE_API_KEY=your-hf-api-key

# Channel info
CHANNEL_NAME=Your Channel Name
```

### Step 4: Verify Installation

```bash
python setup.py
```

This checks:
- ✅ Python version
- ✅ FFmpeg installation
- ✅ Directory structure
- ✅ Dependencies
- ✅ Configuration files

### Step 5: Run System Test

```bash
python test_system.py
```

This tests:
- ✅ All imports
- ✅ Configuration loading
- ✅ Script generation
- ✅ Voice generation
- ✅ FFmpeg availability

## 🔑 API Keys Setup (Optional)

### YouTube API (Required for Upload)

1. **Go to Google Cloud Console**
   - https://console.cloud.google.com/

2. **Create New Project**
   - Click "Select a project" → "New Project"
   - Name: "YouTube Automation"
   - Click "Create"

3. **Enable YouTube Data API v3**
   - Go to "APIs & Services" → "Library"
   - Search "YouTube Data API v3"
   - Click "Enable"

4. **Create OAuth Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "YouTube Automation"
   - Click "Create"

5. **Download Credentials**
   - Click download icon (⬇️)
   - Save as `client_secret.json`
   - Move to project root folder

6. **First Authentication**
   ```bash
   python main.py --mode single
   ```
   - Browser opens automatically
   - Sign in to Google account
   - Grant permissions
   - Token saved to `token.pickle`

### Pexels API (Optional - Better Images)

1. **Sign Up**
   - Go to https://www.pexels.com/api/
   - Click "Get Started"
   - Create free account

2. **Get API Key**
   - Go to your account
   - Copy API key

3. **Add to .env**
   ```env
   PEXELS_API_KEY=your-key-here
   ```

**Free Tier: 200 requests/hour**

### Hugging Face API (Optional - AI Scripts)

1. **Sign Up**
   - Go to https://huggingface.co/
   - Create free account

2. **Get Token**
   - Go to Settings → Access Tokens
   - Create new token
   - Copy token

3. **Add to .env**
   ```env
   HUGGINGFACE_API_KEY=your-token-here
   ```

**Free Tier: Unlimited (rate limited)**

## ✅ Verification

### Quick Test

```bash
# Generate video without upload
python main.py --mode single --no-upload
```

**Expected output:**
```
🎬 YOUTUBE AUTOMATION - STARTING
📝 Step 1/6: Generating script...
✅ Script: 10 Dark Psychology Facts That Will Shock You
🎤 Step 2/6: Generating voiceover...
✅ Audio: 480.50 seconds
🎨 Step 3/6: Generating images...
✅ Images: 18 generated
🎬 Step 4/6: Assembling video...
✅ Video: data/videos/psychology_facts_20240115_143022.mp4
🖼️ Step 5/6: Creating thumbnail...
✅ Thumbnail: data/thumbnails/psychology_facts_20240115_143022.jpg
⏭️ Step 6/6: Skipped (--no-upload flag)
✅ VIDEO GENERATION COMPLETE!
```

### Check Output

```bash
# Windows
dir data\videos
dir data\thumbnails

# Linux/Mac
ls data/videos
ls data/thumbnails
```

## 🐛 Troubleshooting

### Python Not Found

**Error:** `'python' is not recognized`

**Solution:**
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python310\python.exe`
- Or use `python3` instead of `python`

### FFmpeg Not Found

**Error:** `FileNotFoundError: ffmpeg`

**Solution:**
1. Install FFmpeg (see Prerequisites)
2. Add to system PATH
3. Restart terminal
4. Verify: `ffmpeg -version`

### Permission Denied (Linux/Mac)

**Error:** `Permission denied`

**Solution:**
```bash
chmod +x run.sh
sudo chown -R $USER:$USER youtube-automation/
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'edge_tts'`

**Solution:**
```bash
# Activate venv first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall
pip install -r requirements.txt
```

### MoviePy Errors

**Error:** `OSError: [WinError 6]`

**Solution:**
```bash
pip uninstall moviepy
pip install moviepy==1.0.3
```

### SSL Certificate Error

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution:**
```bash
# Windows
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Mac
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Disk Space

**Error:** `No space left on device`

**Solution:**
- Each video: ~500 MB
- Clean old videos: `rm data/videos/*.mp4`
- Or move to external drive

## 🔄 Updating

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Update Project

```bash
git pull origin main
pip install -r requirements.txt
```

## 🗑️ Uninstallation

### Remove Virtual Environment

```bash
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv
```

### Remove Generated Content

```bash
# Windows
rmdir /s data

# Linux/Mac
rm -rf data
```

### Remove Everything

```bash
# Windows
cd ..
rmdir /s youtube-automation

# Linux/Mac
cd ..
rm -rf youtube-automation
```

## 📊 Post-Installation

### Configure Settings

Edit `config/config.yaml`:

```yaml
content:
  niche: "psychology_facts"  # Change niche
  video_length_minutes: 8    # Adjust length

voice:
  voice_name: "en-US-JennyNeural"  # Change voice
  speed: 1.1                       # Adjust speed

images:
  count: 18  # More images = smoother video
```

### Test Different Niches

```bash
python main.py --mode single --niche psychology_facts --no-upload
python main.py --mode single --niche history_mystery --no-upload
python main.py --mode single --niche finance --no-upload
python main.py --mode single --niche reddit_stories --no-upload
```

### Setup Automation

**Windows Task Scheduler:**
- See EXAMPLES.md for detailed steps

**Linux/Mac Cron:**
```bash
crontab -e
# Add: 0 9 * * * cd /path/to/youtube-automation && /path/to/venv/bin/python main.py --mode single
```

## 🎓 Next Steps

1. ✅ Installation complete
2. ✅ Run `python test_system.py`
3. ✅ Generate first video
4. ✅ Review output quality
5. ✅ Adjust configuration
6. ✅ Setup YouTube credentials
7. ✅ Upload test video
8. ✅ Automate production

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - 5-minute guide
- **EXAMPLES.md** - Usage examples
- **PROJECT_SUMMARY.md** - Overview

## 🆘 Getting Help

1. Check `automation.log` for errors
2. Run `python test_system.py`
3. Review troubleshooting section
4. Check individual component tests

---

**Installation complete?** Run: `python main.py --mode single --no-upload`
