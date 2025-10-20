# Usage Examples

Complete examples for every use case.

## 🎯 Basic Usage

### Generate Single Video (No Upload)

```bash
python main.py --mode single --no-upload
```

**Output:**
- Script: `data/scripts/psychology_facts_20240115_143022.txt`
- Audio: `data/audio/psychology_facts_20240115_143022.mp3`
- Images: `data/images/psychology_facts_20240115_143022/`
- Video: `data/videos/psychology_facts_20240115_143022.mp4`
- Thumbnail: `data/thumbnails/psychology_facts_20240115_143022.jpg`

### Generate and Upload

```bash
python main.py --mode single
```

First run opens browser for YouTube authentication.

### Specific Niche

```bash
# Psychology facts
python main.py --mode single --niche psychology_facts

# History mysteries
python main.py --mode single --niche history_mystery

# Finance tips
python main.py --mode single --niche finance

# Reddit stories
python main.py --mode single --niche reddit_stories
```

## 📦 Batch Generation

### Generate 5 Videos

```bash
python main.py --mode batch --count 5 --no-upload
```

### Generate 10 Finance Videos

```bash
python main.py --mode batch --count 10 --niche finance --no-upload
```

### Generate and Upload 3 Videos

```bash
python main.py --mode batch --count 3 --niche psychology_facts
```

## 🔒 Privacy Settings

### Upload as Unlisted (Testing)

```bash
python main.py --mode single --privacy unlisted
```

### Upload as Private

```bash
python main.py --mode single --privacy private
```

### Upload as Public

```bash
python main.py --mode single --privacy public
```

## 🎨 Customization Examples

### Custom Voice

Edit `config/config.yaml`:

```yaml
voice:
  provider: "edge-tts"
  voice_name: "en-US-JennyNeural"  # Female voice
  speed: 1.2  # Faster speech
```

### More Images

```yaml
images:
  count: 25  # More images = smoother video
  ken_burns: true  # Enable zoom/pan effects
```

### Longer Videos

```yaml
content:
  video_length_minutes: 10  # 10-minute videos
```

### Different Resolution

```yaml
video:
  resolution: "1280x720"  # 720p instead of 1080p
  fps: 24  # Cinematic frame rate
```

## 🔧 Advanced Usage

### Test Individual Components

```bash
# Test script generation only
python -m src.script_generator

# Test voice generation only
python -m src.voice_generator

# Test image generation only
python -m src.image_generator

# Test YouTube authentication
python -m src.uploader
```

### Run System Tests

```bash
python test_system.py
```

### Run Setup Check

```bash
python setup.py
```

## 🚀 Windows Quick Commands

```bash
# Single video
run.bat

# System test
run.bat test

# Setup check
run.bat setup

# Batch (5 videos)
run.bat batch 5
```

## 🐧 Linux/Mac Quick Commands

```bash
# Make executable (first time)
chmod +x run.sh

# Single video
./run.sh

# System test
./run.sh test

# Setup check
./run.sh setup

# Batch (10 videos)
./run.sh batch 10
```

## 📅 Automation Examples

### Windows Task Scheduler

**Daily at 9 AM:**

1. Open Task Scheduler
2. Create Basic Task
3. Name: "YouTube Automation"
4. Trigger: Daily, 9:00 AM
5. Action: Start a program
6. Program: `C:\path\to\youtube-automation\venv\Scripts\python.exe`
7. Arguments: `C:\path\to\youtube-automation\main.py --mode single`
8. Start in: `C:\path\to\youtube-automation`

### Linux/Mac Cron

**Daily at 9 AM:**

```bash
# Edit crontab
crontab -e

# Add line
0 9 * * * cd /path/to/youtube-automation && /path/to/venv/bin/python main.py --mode single >> /path/to/logs/cron.log 2>&1
```

**Every 6 hours:**

```bash
0 */6 * * * cd /path/to/youtube-automation && /path/to/venv/bin/python main.py --mode single
```

**3 videos per day (8 AM, 2 PM, 8 PM):**

```bash
0 8,14,20 * * * cd /path/to/youtube-automation && /path/to/venv/bin/python main.py --mode single
```

## 🎬 Production Workflow

### Week 1: Testing Phase

```bash
# Day 1-2: Generate test videos
python main.py --mode batch --count 10 --no-upload

# Review all videos
# Adjust config based on quality

# Day 3-4: Test uploads
python main.py --mode single --privacy unlisted
# Check YouTube Studio for quality

# Day 5-7: Small batch
python main.py --mode batch --count 3 --privacy public
# Monitor performance
```

### Week 2+: Production

```bash
# Daily generation (automated via cron/Task Scheduler)
python main.py --mode single --niche psychology_facts

# Weekly batch for buffer
python main.py --mode batch --count 7 --no-upload
# Review and upload manually
```

## 🔄 Multi-Channel Strategy

### Channel 1: Psychology

```bash
# config/config_psychology.yaml
python main.py --mode single --niche psychology_facts
```

### Channel 2: Finance

```bash
# config/config_finance.yaml
python main.py --mode single --niche finance
```

### Channel 3: History

```bash
# config/config_history.yaml
python main.py --mode single --niche history_mystery
```

## 📊 Analytics Workflow

### Generate with Tracking

```bash
# Generate video
python main.py --mode single

# Check logs/videos.json for video_id
cat logs/videos.json | grep youtube_id

# Monitor in YouTube Studio
# Track: Views, CTR, Watch Time, Revenue
```

## 🐛 Debugging Examples

### Verbose Logging

Edit `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Test Without Effects

Edit `config/config.yaml`:

```yaml
images:
  ken_burns: false  # Disable effects
  transition_duration: 0  # No transitions
```

### Use Fallback Voice

```yaml
voice:
  provider: "gtts"  # Force gTTS instead of Edge TTS
```

### Minimal Images (Faster)

```yaml
images:
  count: 10  # Fewer images = faster generation
```

## 💡 Pro Tips

### Tip 1: Generate Overnight

```bash
# Generate 20 videos overnight
nohup python main.py --mode batch --count 20 --no-upload &
```

### Tip 2: Different Niches Daily

```bash
# Monday: Psychology
python main.py --mode single --niche psychology_facts

# Tuesday: Finance
python main.py --mode single --niche finance

# Wednesday: History
python main.py --mode single --niche history_mystery
```

### Tip 3: A/B Test Thumbnails

```python
# In thumbnail_creator.py
variants = creator.create_multiple_variants(
    image_path, 
    title, 
    output_dir, 
    count=3  # Generate 3 variants
)
```

### Tip 4: Batch Review

```bash
# Generate 10 videos
python main.py --mode batch --count 10 --no-upload

# Review in VLC/Media Player
# Upload best ones manually
```

### Tip 5: Schedule Different Times

```bash
# Morning: Psychology (high engagement)
0 8 * * * python main.py --niche psychology_facts

# Afternoon: Finance (work hours)
0 14 * * * python main.py --niche finance

# Evening: Stories (leisure time)
0 20 * * * python main.py --niche reddit_stories
```

## 🎯 Goal-Based Examples

### Goal: 100 Videos in 30 Days

```bash
# Generate 4 videos daily
python main.py --mode batch --count 4 --no-upload

# Review and upload 3-4 per day
```

### Goal: Multiple Niches

```bash
# 2 psychology + 1 finance daily
python main.py --mode batch --count 2 --niche psychology_facts
python main.py --mode single --niche finance
```

### Goal: High Quality Only

```bash
# Generate 5, pick best 1
python main.py --mode batch --count 5 --no-upload
# Manual review and upload
```

## 📈 Scaling Examples

### Scale to 10 Videos/Day

```bash
# Morning batch
python main.py --mode batch --count 5 --no-upload

# Evening batch
python main.py --mode batch --count 5 --no-upload

# Review and schedule uploads
```

### Scale to Multiple Channels

```bash
# Channel 1
cd channel1 && python main.py --mode single

# Channel 2
cd channel2 && python main.py --mode single

# Channel 3
cd channel3 && python main.py --mode single
```

---

**Need more examples?** Check `README.md` for full documentation.
