"""Authenticate YouTube locally and generate token.pickle"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate():
    """Authenticate and save token.pickle"""
    creds = None
    
    if os.path.exists('token.pickle'):
        print("Loading existing token.pickle...")
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
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            if not os.path.exists('client_secret.json'):
                print("ERROR: client_secret.json not found!")
                return False
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        print("Saving token.pickle...")
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    print("\n" + "="*60)
    print("✅ Authentication successful!")
    print("="*60)
    print("\ntoken.pickle has been created.")
    print("\nNext steps:")
    print("1. Commit token.pickle to GitHub (it's in .gitignore, so add manually)")
    print("2. Or upload as GitHub Secret")
    print("="*60)
    
    return True

if __name__ == '__main__':
    authenticate()
