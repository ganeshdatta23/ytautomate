"""Extract refresh token from token.pickle for GitHub Actions"""
import pickle
import os

def extract_refresh_token():
    """Extract refresh token from existing token.pickle"""
    if not os.path.exists('token.pickle'):
        print("❌ token.pickle not found. Run authentication first.")
        return
    
    try:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        
        if hasattr(creds, 'refresh_token') and creds.refresh_token:
            print("✅ Refresh token extracted successfully!")
            print("\nAdd this to your GitHub Secrets as YOUTUBE_REFRESH_TOKEN:")
            print(f"{creds.refresh_token}")
            print("\nAlso make sure you have these secrets:")
            print("- YOUTUBE_CLIENT_ID")
            print("- YOUTUBE_CLIENT_SECRET")
            print("- YOUTUBE_REFRESH_TOKEN (the token above)")
        else:
            print("❌ No refresh token found in credentials")
            
    except Exception as e:
        print(f"❌ Error reading token.pickle: {e}")

if __name__ == '__main__':
    extract_refresh_token()