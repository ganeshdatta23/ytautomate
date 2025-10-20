# 🚀 Quick Start Guide

Get your first YouTube video generated in 5 minutes!

## Step 1: Install FFmpeg (Required)

### Windows
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Restart terminal and verify: `ffmpeg -version`

### Linux
```bash
sudo apt update && sudo apt install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

## Step 2: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run Setup Check

```bash
python setup.py
```

This will verify everything is installed correctly.

## Step 4: Configure (Optional)

Edit `config/config.yaml` to customize:
- Niche (psychology_facts, history_mystery, finance, reddit_stories)
- Voice (en-US-GuyNeural for male, en-US-JennyNeural for female)
- Video settings

## Step 5: Generate Your First Video

```bash
# Generate without uploading (for testing)
python main.py --mode single --no-upload
```

This will:
1. ✅ Generate script (8 minutes)
2. ✅ Create voiceover (Edge TTS)
3. ✅ Download 18 images
4. ✅ Assemble video with effects
5. ✅ Create thumbnail
6. ⏭️ Skip upload

**Output:** `data/videos/psychology_facts_YYYYMMDD_HHMMSS.mp4`

## Step 6: Review Your Video

1. Open `data/videos/` folder
2. Watch the generated video
3. Check `data/thumbnails/` for thumbnail

## Step 7: Setup YouTube Upload (Optional)

### Get YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "YouTube Automation"
3. Enable **YouTube Data API v3**
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Application type: Desktop app
6. Download JSON as `client_secret.json`
7. Place in project root

### First Upload

```bash
# Upload as unlisted (for testing)
python main.py --mode single --privacy unlisted
```

Browser will open for authentication. After first time, token is saved.

## Step 8: Generate Multiple Videos

```bash
# Generate 5 videos
python main.py --mode batch --count 5 --no-upload

# Specific niche
python main.py --mode single --niche finance

# Upload as public
python main.py --mode single --privacy public
```

## 🎯 Available Niches

- `psychology_facts` - Dark psychology, human behavior
- `history_mystery` - Unsolved mysteries, ancient secrets  
- `finance` - Money tips, investing, wealth
- `reddit_stories` - Dramatic Reddit tales

## 🎤 Voice Options

Edit `config/config.yaml`:

```yaml
voice:
  provider: "edge-tts"
  voice_name: "en-US-GuyNeural"  # Male
  # voice_name: "en-US-JennyNeural"  # Female
  # voice_name: "en-GB-RyanNeural"  # British
  speed: 1.1
```

## 🎨 Customize Images

Add Pexels API key to `.env` for better images:

```env
PEXELS_API_KEY=your-key-here
```

Get free key: https://www.pexels.com/api/

## 📊 Monitor Progress

```bash
# View generation log
cat logs/videos.json

# Check automation log
cat automation.log
```

## ⚡ Pro Tips

1. **Test First**: Always use `--no-upload` initially
2. **Review Output**: Check video quality before uploading
3. **Adjust Config**: Tweak settings based on results
4. **Use Unlisted**: Test uploads as unlisted first
5. **Batch Generate**: Create multiple videos, review, then upload

## 🐛 Common Issues

### "FFmpeg not found"
- Install FFmpeg and add to PATH
- Restart terminal after installation

### "client_secret.json not found"
- Only needed for YouTube upload
- Generate videos with `--no-upload` flag

### "Edge TTS failed"
- System automatically falls back to gTTS
- Check internet connection

### Video too short/long
- Edit `config/config.yaml` → `video_length_minutes`
- Adjust `images.count` for pacing

## 🚀 Next Steps

1. ✅ Generate first video
2. ✅ Review and adjust settings
3. ✅ Setup YouTube credentials
4. ✅ Upload test video (unlisted)
5. ✅ Generate batch of videos
6. ✅ Automate with cron/Task Scheduler

## 📚 Full Documentation

See `README.md` for complete documentation.

---

**Ready to automate? Run:** `python main.py --mode single --no-upload`
