# YouTube Authentication Setup Guide

## 🚨 IMPORTANT: You Must Add Test User First

Your YouTube automation cannot work until you add yourself as a test user in Google Cloud Console.

---

## Step 1: Add Test User (REQUIRED)

### Option A: Using Web Browser (Recommended)

1. **Open this link:**
   https://console.cloud.google.com/apis/credentials/consent?project=youtube-automation-475701

2. **Click "EDIT APP"** (blue button at top)

3. **Scroll down to "Test users" section**

4. **Click "+ ADD USERS"**

5. **Enter your email:**
   ```
   padamataganeshdatta@gmail.com
   ```

6. **Click "ADD"**

7. **Click "SAVE"** at bottom of page

8. **Click "SAVE AND CONTINUE"** if prompted

✅ **Done!** You should now see your email listed under "Test users"

---

## Step 2: Authenticate Locally

After adding test user, run this on your local machine:

```bash
cd d:\yt-automation\youtube-automation
call venv\Scripts\activate
python authenticate_youtube.py
```

**What happens:**
- Browser opens automatically
- Sign in with: `padamataganeshdatta@gmail.com`
- Grant permissions
- `token.pickle` file is created
- ✅ Authentication complete!

---

## Step 3: Upload token.pickle to GitHub

### Option A: As Repository Secret (Recommended)

1. **Encode token.pickle to base64:**

```bash
# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("token.pickle")) | Out-File token_base64.txt

# Or Python
python -c "import base64; print(base64.b64encode(open('token.pickle','rb').read()).decode())" > token_base64.txt
```

2. **Copy content of token_base64.txt**

3. **Add to GitHub Secrets:**
   - Go to: https://github.com/ganeshdatta23/yt-automation/settings/secrets/actions
   - Click "New repository secret"
   - Name: `YOUTUBE_TOKEN_PICKLE_BASE64`
   - Value: Paste the base64 content
   - Click "Add secret"

### Option B: Commit to Repository (Less Secure)

```bash
# Remove token.pickle from .gitignore temporarily
git add -f token.pickle
git commit -m "Add YouTube authentication token"
git push origin main
```

⚠️ **Warning:** This exposes your token publicly. Use Option A instead.

---

## Step 4: Update GitHub Actions Workflow

The workflow needs to decode the token. I'll update it automatically.

---

## Troubleshooting

### Error: "Access blocked: has not completed Google verification"
**Solution:** You didn't add test user. Go back to Step 1.

### Error: "could not locate runnable browser"
**Solution:** You're trying to authenticate in GitHub Actions (headless). Must authenticate locally first (Step 2).

### Error: "Expecting value: line 2 column 1"
**Solution:** `client_secret.json` is malformed. Run `python generate_secret_json.py` and update GitHub secret.

---

## Why This is Necessary

1. **Google OAuth requires browser** - Can't authenticate in GitHub Actions directly
2. **App is in Testing mode** - Only test users can authenticate
3. **token.pickle stores credentials** - Allows GitHub Actions to upload without browser

---

## Summary

1. ✅ Add test user in Google Cloud Console (web UI only)
2. ✅ Run `python authenticate_youtube.py` locally
3. ✅ Upload `token.pickle` to GitHub as secret
4. ✅ GitHub Actions can now upload videos automatically

---

**Current Status:** ❌ Test user not added yet

**Next Step:** Click this link and add test user:
https://console.cloud.google.com/apis/credentials/consent?project=youtube-automation-475701
