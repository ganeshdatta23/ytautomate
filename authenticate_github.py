"""GitHub Actions Authentication Script"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def create_client_secret():
    """Create client_secret.json from environment variable"""
    client_secret_json = os.getenv('YOUTUBE_CLIENT_SECRET_JSON')
    if client_secret_json:
        with open('client_secret.json', 'w') as f:
            f.write(client_secret_json)
        return True
    return False

def authenticate():
    """Authenticate and save token.pickle"""
    if not create_client_secret():
        print("❌ Error: YOUTUBE_CLIENT_SECRET_JSON environment variable not found")
        return False
        
    creds = None
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        except (EOFError, pickle.UnpicklingError) as pe:
            print(f"ERROR: token.pickle is corrupted or empty: {pe}")
            print("Removing corrupted token.pickle so a fresh authentication can run...")
            try:
                os.remove('token.pickle')
            except Exception:
                print("Could not remove token.pickle automatically. Please delete it manually and retry.")
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🔐 Starting new authentication flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print("✅ New token.pickle created!")
    
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        response = youtube.channels().list(part='snippet', mine=True).execute()
        print(f"✅ Successfully authenticated as: {response['items'][0]['snippet']['title']}")
        return True
    except Exception as e:
        print(f"❌ Authentication test failed: {str(e)}")
        return False

if __name__ == '__main__':
    authenticate()