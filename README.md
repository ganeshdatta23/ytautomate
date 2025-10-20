# 🎬 YouTube Automation System

**Automated YouTube video generation and upload system using AI** - Generate unique videos daily with Gemini AI, free TTS, and automated scheduling. Zero cost, production-ready.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-green.svg)](https://github.com/features/actions)

> Generate professional YouTube videos automatically with AI-powered scripts, voice synthesis, and image generation - all for free!

## 🚀 Features

- **Script Generation**: AI-powered scripts using Ollama, Hugging Face, or template-based fallback
- **Voice Generation**: Multiple TTS providers (Edge TTS, gTTS, pyttsx3) with automatic fallback
- **Image Generation**: Free APIs (Pollinations.ai, Unsplash, Pexels) with fallback
- **Video Assembly**: FFmpeg-based with Ken Burns effects, transitions, and audio sync
- **Thumbnail Creation**: Eye-catching thumbnails with text overlays
- **YouTube Upload**: Automated upload with metadata, tags, and thumbnails
- **Multiple Niches**: Psychology facts, history mysteries, finance tips, Reddit stories

## 📋 Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **FFmpeg** (required for video processing)
   
   **Windows:**
   - Download from https://ffmpeg.org/download.html
   - Extract and add to PATH
   - Verify: `ffmpeg -version`
   
   **Linux:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```

### API Keys (Optional but Recommended)

1. **YouTube Data API v3** (Required for upload)
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download `client_secret.json` to project root

2. **Pexels API** (Optional - for better images)
   - Sign up at https://www.pexels.com/api/
   - Free tier: 200 requests/hour
   - Add to `.env` file

3. **Hugging Face API** (Optional - for AI scripts)
   - Sign up at https://huggingface.co/
   - Get API token from settings
   - Add to `.env` file

## 🛠️ Installation

### 1. Clone/Download Project

```bash
cd youtube-automation
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
YOUTUBE_CLIENT_ID=your-client-id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your-client-secret
PEXELS_API_KEY=your-pexels-api-key
HUGGINGFACE_API_KEY=your-hf-api-key
CHANNEL_NAME=Your Channel Name
```

### 5. Setup YouTube Credentials

1. Download `client_secret.json` from Google Cloud Console
2. Place in project root directory
3. First run will open browser for OAuth authentication
4. Token saved to `token.pickle` for future use

## 🎯 Usage

### Single Video Generation

```bash
# Generate one video (default niche)
python main.py --mode single

# Specific niche
python main.py --mode single --niche psychology_facts

# Generate without uploading (for review)
python main.py --mode single --no-upload

# Upload as unlisted (for testing)
python main.py --mode single --privacy unlisted
```

### Batch Generation

```bash
# Generate 10 videos
python main.py --mode batch --count 10

# Specific niche
python main.py --mode batch --count 5 --niche finance

# Generate without uploading
python main.py --mode batch --count 3 --no-upload
```

### Available Niches

- `psychology_facts` - Dark psychology, human behavior
- `history_mystery` - Unsolved mysteries, ancient secrets
- `finance` - Money tips, investing, wealth building
- `reddit_stories` - Dramatic Reddit tales, AITA stories

## ⚙️ Configuration

### config/config.yaml

```yaml
content:
  niche: "psychology_facts"
  video_length_minutes: 8
  videos_per_day: 3

voice:
  provider: "edge-tts"  # edge-tts, gtts, pyttsx3
  voice_name: "en-US-GuyNeural"  # or en-US-JennyNeural
  speed: 1.1

images:
  count: 18
  style: "cinematic, professional, 4k, dramatic lighting"
  transition_duration: 0.5
  ken_burns: true

video:
  resolution: "1920x1080"
  fps: 30
  codec: "libx264"
  bitrate: "8M"
  background_music_volume: 0.2

youtube:
  category: 22  # People & Blogs
  language: "en"
  privacy: "public"
  made_for_kids: false
```

### Available Voice Options

**Edge TTS Voices (Best Quality):**
- `en-US-GuyNeural` - Male, natural
- `en-US-JennyNeural` - Female, natural
- `en-GB-RyanNeural` - British male
- `en-AU-NatashaNeural` - Australian female

## 📁 Project Structure

```
youtube-automation/
├── src/
│   ├── script_generator.py    # AI script generation
│   ├── voice_generator.py     # TTS with fallback
│   ├── image_generator.py     # Free image APIs
│   ├── video_assembler.py     # FFmpeg video creation
│   ├── thumbnail_creator.py   # Thumbnail design
│   └── uploader.py            # YouTube API upload
├── config/
│   ├── config.yaml            # Main configuration
│   └── prompts.yaml           # Niche templates
├── data/
│   ├── scripts/               # Generated scripts
│   ├── audio/                 # Voiceovers
│   ├── images/                # Downloaded images
│   ├── videos/                # Final videos
│   └── thumbnails/            # Thumbnails
├── logs/
│   └── videos.json            # Generation log
├── main.py                    # Main automation
├── requirements.txt           # Dependencies
├── .env                       # API keys
└── README.md                  # This file
```

## 🔧 Troubleshooting

### FFmpeg Not Found

**Error:** `FileNotFoundError: [WinError 2] The system cannot find the file specified`

**Solution:**
1. Install FFmpeg (see Prerequisites)
2. Add to system PATH
3. Restart terminal/IDE
4. Verify: `ffmpeg -version`

### YouTube Upload Failed

**Error:** `client_secret.json not found`

**Solution:**
1. Download OAuth credentials from Google Cloud Console
2. Save as `client_secret.json` in project root
3. Run again - browser will open for authentication

### Image Generation Slow

**Issue:** Pollinations.ai timeout

**Solution:**
1. Add Pexels API key to `.env`
2. System will automatically use Pexels as fallback
3. Or use Unsplash (no API key needed)

### Voice Generation Failed

**Issue:** Edge TTS not working

**Solution:**
- System automatically falls back to gTTS
- Then to pyttsx3 (offline)
- Check internet connection for Edge TTS

### MoviePy Errors

**Error:** `OSError: [WinError 6] The handle is invalid`

**Solution:**
```bash
pip uninstall moviepy
pip install moviepy==1.0.3
```

## 🚀 Advanced Usage

### Test Individual Components

```bash
# Test script generation
python -m src.script_generator

# Test voice generation
python -m src.voice_generator

# Test image generation
python -m src.image_generator

# Test video assembly
python -m src.video_assembler

# Test thumbnail creation
python -m src.thumbnail_creator

# Test YouTube authentication
python -m src.uploader
```

### Custom Niche

Edit `config/prompts.yaml` to add your own niche:

```yaml
your_niche:
  title_templates:
    - "Your Title Template {topic}"
  
  topics:
    - "topic 1"
    - "topic 2"
  
  script_prompt: |
    Your custom script prompt here...
```

Then use:

```bash
python main.py --mode single --niche your_niche
```

## 📊 Monitoring

### View Generation Log

```bash
# View all generated videos
cat logs/videos.json

# Count successful uploads
python -c "import json; data=json.load(open('logs/videos.json')); print(f'Total: {len(data)}')"
```

### Check Output Files

```bash
# List generated videos
ls data/videos/

# Check video duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 data/videos/your_video.mp4
```

## 🔄 Automation

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `C:\path\to\main.py --mode single`

### Linux/Mac Cron

```bash
# Edit crontab
crontab -e

# Add daily job at 9 AM
0 9 * * * cd /path/to/youtube-automation && /path/to/venv/bin/python main.py --mode single
```

### GitHub Actions (Free)

See `.github/workflows/auto-upload.yml` for automated cloud execution.

## 💡 Best Practices

### Content Strategy

1. **Consistency**: Upload 3-5 videos per week
2. **Niche Focus**: Stick to 1-2 niches initially
3. **SEO**: Use all 30 tags, detailed descriptions
4. **Thumbnails**: High contrast, bold text, faces
5. **Titles**: Include numbers, emotions, keywords

### Quality Control

1. **Review First**: Use `--no-upload` flag initially
2. **Test Voices**: Try different voice options
3. **Check Duration**: Aim for 8-10 minutes
4. **Verify Audio**: Ensure voice is clear
5. **Thumbnail Test**: Create multiple variants

### Monetization

1. **Watch Time**: Longer videos = more revenue
2. **CTR**: Better thumbnails = more clicks
3. **Retention**: Engaging scripts = longer watch time
4. **Consistency**: Regular uploads = algorithm boost
5. **Niche**: Some niches pay more (finance > entertainment)

## 📈 Scaling

### Multiple Channels

1. Create separate config files
2. Use different `.env` files
3. Separate `client_secret.json` per channel
4. Run in different directories

### Bulk Generation

```bash
# Generate 50 videos (no upload)
python main.py --mode batch --count 50 --no-upload

# Review and upload manually
# Or upload in batches
```

### Cloud Deployment

**AWS Lambda:**
- Package as Lambda function
- Trigger via CloudWatch Events
- Store videos in S3

**Google Cloud Functions:**
- Deploy as Cloud Function
- Schedule with Cloud Scheduler
- 2M free invocations/month

## 🐛 Known Issues

1. **MoviePy Memory**: Large batches may consume RAM
   - Solution: Generate in smaller batches
   
2. **API Rate Limits**: Pexels has 200/hour limit
   - Solution: System uses Pollinations as primary
   
3. **YouTube Quota**: 10,000 units/day limit
   - Solution: ~6 uploads per day max

## 📝 License

This project is for educational purposes. Ensure compliance with:
- YouTube Terms of Service
- API provider terms
- Copyright laws for content

## 🤝 Support

For issues:
1. Check troubleshooting section
2. Review logs in `automation.log`
3. Test individual components
4. Verify API keys and credentials

## 🎓 Learning Resources

- [YouTube Creator Academy](https://creatoracademy.youtube.com/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

## 🚀 Next Steps

1. Generate your first video: `python main.py --mode single --no-upload`
2. Review output in `data/videos/`
3. Adjust config based on results
4. Upload test video: `python main.py --mode single --privacy unlisted`
5. Scale to batch production

---

**Happy Automating! 🎬**
