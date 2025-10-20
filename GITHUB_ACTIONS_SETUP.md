# 🤖 GitHub Actions - Automated Daily Video Upload

## ⏰ Schedule: Daily at 11 AM IST

Your repository is configured to automatically generate and upload YouTube videos every day at 11 AM IST.

## 🔧 Setup Instructions

### Step 1: Add Repository Secrets

Go to your GitHub repository:
**https://github.com/ganeshdatta23/yt-automation**

1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets one by one:

#### Required Secrets:

**YOUTUBE_CLIENT_ID**
```
Your-YouTube-Client-ID.apps.googleusercontent.com
```

**YOUTUBE_CLIENT_SECRET**
```
Your-YouTube-Client-Secret
```

**YOUTUBE_CLIENT_SECRET_JSON**
```json
{"installed":{"client_id":"your-client-id","project_id":"your-project","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"your-secret","redirect_uris":["http://localhost"]}}
```

**PEXELS_API_KEY**
```
Your-Pexels-API-Key
```

**GEMINI_API_KEY**
```
Your-Gemini-API-Key
```

**HUGGINGFACE_API_KEY**
```
Your-HuggingFace-API-Key
```

**CHANNEL_NAME**
```
Your Channel Name
```

### Step 2: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The workflow will now run automatically

### Step 3: Test Manual Run (Optional)

1. Go to **Actions** tab
2. Click **"Auto Generate YouTube Video"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it generate and upload a video!

## 📅 Schedule Details

- **Time:** 11:00 AM IST (5:30 AM UTC)
- **Frequency:** Daily
- **Action:** Generate 1 video and upload to YouTube
- **Cost:** FREE (GitHub gives 2000 minutes/month)

## 🎬 What Happens Daily

1. ✅ Fetches trending topic using Gemini AI
2. ✅ Generates unique script with Gemini
3. ✅ Creates voiceover (gTTS)
4. ✅ Downloads 18 images (Pollinations/Pexels)
5. ✅ Assembles video with transitions
6. ✅ Creates thumbnail
7. ✅ Uploads to YouTube automatically

## 📊 Monitoring

### View Workflow Runs:
**https://github.com/ganeshdatta23/yt-automation/actions**

### Check Logs:
- Click on any workflow run
- View detailed logs for each step
- See if upload succeeded

### Email Notifications:
- GitHub sends email if workflow fails
- Check your GitHub email settings

## ⚙️ Customization

### Change Upload Time:

Edit `.github/workflows/auto-upload.yml`:

```yaml
schedule:
  - cron: '30 5 * * *'  # 11 AM IST
```

**Cron format:** `minute hour day month weekday`

Examples:
- `0 0 * * *` - Midnight UTC (5:30 AM IST)
- `0 12 * * *` - Noon UTC (5:30 PM IST)
- `0 6,18 * * *` - 6 AM & 6 PM UTC (11:30 AM & 11:30 PM IST)

### Change Niche:

Edit `config/config.yaml` in repository:

```yaml
content:
  niche: "finance"  # psychology_facts, history_mystery, finance, reddit_stories
```

### Upload Multiple Videos Daily:

Edit workflow file:

```yaml
- name: Generate and upload video
  run: |
    python main.py --mode batch --count 3
```

## 🔒 Security Notes

- ✅ API keys stored as GitHub Secrets (encrypted)
- ✅ Not visible in logs
- ✅ Not accessible to public
- ✅ Only workflow can access them

## 🐛 Troubleshooting

### Workflow Not Running?

1. Check if Actions are enabled
2. Verify all secrets are added
3. Check workflow file syntax

### Upload Failed?

1. Check YouTube API quota (10,000/day)
2. Verify OAuth credentials
3. Check workflow logs for errors

### Video Quality Issues?

1. Adjust `config/config.yaml` settings
2. Change image count, resolution, etc.
3. Push changes to GitHub

## 💰 Cost Breakdown

- **GitHub Actions:** FREE (2000 min/month)
- **Video generation:** ~10 min/video
- **Monthly capacity:** 200 videos FREE
- **Your usage:** 30 videos/month (1 daily)
- **Cost:** ₹0

## 🚀 Scaling Up

### 3 Videos Per Day:

```yaml
schedule:
  - cron: '30 5 * * *'   # 11 AM IST
  - cron: '30 11 * * *'  # 5 PM IST
  - cron: '30 17 * * *'  # 11 PM IST
```

### Different Niches:

Create multiple workflow files:
- `psychology-daily.yml`
- `finance-daily.yml`
- `history-daily.yml`

## 📈 Expected Results

- **Videos uploaded:** 30/month
- **Watch time:** ~240 minutes/month (8 min × 30)
- **Views (estimated):** 1,000-5,000/month
- **Revenue (estimated):** $20-$100/month

## ✅ Verification Checklist

- [ ] All 7 secrets added to GitHub
- [ ] GitHub Actions enabled
- [ ] Workflow file committed
- [ ] Manual test run successful
- [ ] First automated upload completed
- [ ] YouTube channel receiving videos

## 🎉 You're All Set!

Your YouTube channel will now receive:
- ✅ 1 new video daily at 11 AM IST
- ✅ Unique content every time (Gemini AI)
- ✅ Fully automated (no manual work)
- ✅ 100% free forever

**Next video uploads:** Tomorrow at 11 AM IST! 🚀

---

**Repository:** https://github.com/ganeshdatta23/yt-automation
**Workflow:** https://github.com/ganeshdatta23/yt-automation/actions
