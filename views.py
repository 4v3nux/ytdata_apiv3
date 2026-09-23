import os
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

VIDEO_ID = "id" 
UPDATE_INTERVAL = 600 # 600 sec = 10 min (for optimization)
TOKEN_FILE = "token.json"  # authorization 

def get_authenticated_service():
    """Authorization via saved token.json or local browser (if the file doesn't exist)"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
                
        if not creds:
        # If running on a PC, a browser will open.
        # On a server, this block will throw an error if token.json has not been transferred from a PC in advance!
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            print(f"File {TOKEN_FILE} successfully saved/updated.")

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def update_video_title():
    try:
        youtube = get_authenticated_service()
        
        print(f"Starting periodic update for video ID: {VIDEO_ID}")
        print(f"Update interval: every {UPDATE_INTERVAL // 60} minutes.\n")

        while True:
            video_response = youtube.videos().list(
                part="snippet,statistics",
                id=VIDEO_ID
            ).execute()

            if not video_response.get("items"):
                print("Error: Video with this ID not found!")
                break

            item = video_response["items"][0]
            statistics = item["statistics"]
            view_count = statistics.get("viewCount", "0")
            like_count = statistics.get("likeCount", "0")
            snippet = item["snippet"]

            new_title = f"This video has {view_count} views and {like_count} likes" # change this for your own if you want
            
            if snippet["title"] == new_title:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data has not changed (Views: {view_count}, Likes: {like_count}). Skip update.")
            else:
                snippet["title"] = new_title
                
                update_request = youtube.videos().update(
                    part="snippet",
                    body={
                        "id": VIDEO_ID,
                        "snippet": snippet
                    }
                )
                update_response = update_request.execute()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Success! New title: {update_response['snippet']['title']}")

            time.sleep(UPDATE_INTERVAL)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_video_title()
