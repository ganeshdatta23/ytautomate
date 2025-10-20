"""YouTube Uploader - Uploads videos using YouTube Data API v3"""
import os
import logging
import pickle
from typing import Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubeUploader:
    def __init__(self, config: dict):
        self.config = config
        self.youtube = None
        self.credentials_file = 'client_secret.json'
        self.token_file = 'token.pickle'
    
    def authenticate(self) -> bool:
        """Authenticate with YouTube API"""
        try:
            creds = None
            
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        logger.error("❌ client_secret.json not found. Download from Google Cloud Console.")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.youtube = build('youtube', 'v3', credentials=creds)
            logger.info("✅ YouTube authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            return False
    
    def upload(self, video_path: str, metadata: Dict, thumbnail_path: Optional[str] = None) -> Optional[str]:
        """Upload video to YouTube"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return None
            
            logger.info(f"📤 Uploading video: {metadata['title']}")
            
            body = {
                'snippet': {
                    'title': metadata['title'],
                    'description': metadata['description'],
                    'tags': metadata['tags'],
                    'categoryId': str(self.config['youtube']['category']),
                    'defaultLanguage': self.config['youtube']['language']
                },
                'status': {
                    'privacyStatus': self.config['youtube']['privacy'],
                    'selfDeclaredMadeForKids': self.config['youtube']['made_for_kids']
                }
            }
            
            media = MediaFileUpload(
                video_path,
                chunksize=1024*1024,
                resumable=True,
                mimetype='video/*'
            )
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")
            
            video_id = response['id']
            logger.info(f"✅ Video uploaded! ID: {video_id}")
            logger.info(f"🔗 URL: https://www.youtube.com/watch?v={video_id}")
            
            if thumbnail_path and os.path.exists(thumbnail_path):
                self._upload_thumbnail(video_id, thumbnail_path)
            
            return video_id
            
        except HttpError as e:
            logger.error(f"❌ Upload failed: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Upload error: {e}")
            return None
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """Upload custom thumbnail"""
        try:
            logger.info("🎨 Uploading thumbnail...")
            
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            )
            
            request.execute()
            logger.info("✅ Thumbnail uploaded")
            return True
            
        except Exception as e:
            logger.error(f"Thumbnail upload error: {e}")
            return False
    
    def update_video(self, video_id: str, updates: Dict) -> bool:
        """Update video metadata"""
        try:
            video = self.youtube.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()
            
            if not video['items']:
                logger.error(f"Video {video_id} not found")
                return False
            
            video_data = video['items'][0]
            
            if 'title' in updates:
                video_data['snippet']['title'] = updates['title']
            if 'description' in updates:
                video_data['snippet']['description'] = updates['description']
            if 'tags' in updates:
                video_data['snippet']['tags'] = updates['tags']
            
            self.youtube.videos().update(
                part='snippet,status',
                body=video_data
            ).execute()
            
            logger.info(f"✅ Video {video_id} updated")
            return True
            
        except Exception as e:
            logger.error(f"Update error: {e}")
            return False


def main():
    """Test uploader"""
    import yaml
    
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    uploader = YouTubeUploader(config)
    
    if uploader.authenticate():
        print("✅ Authentication successful!")
        print("Ready to upload videos")
    else:
        print("❌ Authentication failed")
        print("Make sure client_secret.json is in the project root")


if __name__ == '__main__':
    main()
