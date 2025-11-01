# GitHub Actions Authentication Fix

## Problem
The GitHub Actions workflow was failing with authentication errors:
- `Ran out of input` when reading token.pickle
- `Expecting value: line 2 column 1 (char 1)` JSON parsing error

## Root Cause
The base64 encoding/decoding of token.pickle in GitHub Actions was corrupting the file, causing authentication failures.

## Solution
Switched from pickle file to refresh token authentication for CI/CD environments.

## Setup Steps

### 1. Local Authentication
First, authenticate locally to get the refresh token:

```bash
# Run local authentication
python authenticate_github.py

# Extract refresh token
python extract_refresh_token.py
```

### 2. GitHub Secrets
Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

**Required Secrets:**
- `YOUTUBE_CLIENT_ID` - Your OAuth client ID
- `YOUTUBE_CLIENT_SECRET` - Your OAuth client secret  
- `YOUTUBE_CLIENT_SECRET_JSON` - Full client_secret.json content
- `YOUTUBE_REFRESH_TOKEN` - Refresh token from step 1
- `PEXELS_API_KEY` - Pexels API key (optional)
- `GEMINI_API_KEY` - Gemini API key (optional)
- `HUGGINGFACE_API_KEY` - Hugging Face API key (optional)
- `CHANNEL_NAME` - Your YouTube channel name

### 3. Test the Fix
Trigger the workflow manually:
1. Go to Actions tab in GitHub
2. Select "Auto Generate YouTube Video"
3. Click "Run workflow"

## How It Works

### Local Development
- Uses interactive OAuth flow with `client_secret.json`
- Saves credentials to `token.pickle` for reuse

### GitHub Actions
- Detects CI environment (`GITHUB_ACTIONS=true`)
- Uses refresh token from environment variables
- Bypasses pickle file completely
- Creates fresh access token on each run

## Code Changes

### 1. Enhanced Authentication (`src/uploader.py`)
```python
def authenticate(self) -> bool:
    # Try environment variables first (for CI/CD)
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        creds = self._authenticate_from_env()
        if creds:
            self.youtube = build('youtube', 'v3', credentials=creds)
            return True
    
    # Fallback to local token.pickle...
```

### 2. Environment Authentication
```python
def _authenticate_from_env(self) -> Optional[Credentials]:
    client_id = os.getenv('YOUTUBE_CLIENT_ID')
    client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
    
    if client_id and client_secret and refresh_token:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        creds.refresh(Request())
        return creds
```

### 3. Updated Workflow
```yaml
- name: Setup YouTube authentication
  run: |
    echo "YOUTUBE_REFRESH_TOKEN=${{ secrets.YOUTUBE_REFRESH_TOKEN }}" >> .env
```

## Benefits
- ✅ More reliable authentication in CI/CD
- ✅ No file corruption issues
- ✅ Faster authentication (no pickle loading)
- ✅ Better error handling
- ✅ Maintains backward compatibility for local development

## Troubleshooting

### Error: "Cannot run interactive auth in CI environment"
- Make sure `YOUTUBE_REFRESH_TOKEN` is set in GitHub Secrets
- Verify `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET` are correct

### Error: "Environment authentication failed"
- Check that all three secrets are set: CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
- Ensure refresh token was extracted correctly from local authentication

### Error: "Token refresh failed"
- Refresh token may have expired (rare, but possible)
- Re-run local authentication and extract new refresh token

## Testing Locally
You can test the CI authentication method locally:

```bash
# Set environment variables
export GITHUB_ACTIONS=true
export YOUTUBE_CLIENT_ID="your-client-id"
export YOUTUBE_CLIENT_SECRET="your-client-secret"  
export YOUTUBE_REFRESH_TOKEN="your-refresh-token"

# Test authentication
python -c "from src.uploader import YouTubeUploader; import yaml; config=yaml.safe_load(open('config/config.yaml')); uploader=YouTubeUploader(config); print('✅ Success' if uploader.authenticate() else '❌ Failed')"
```

This fix ensures reliable YouTube authentication in GitHub Actions while maintaining full compatibility with local development.