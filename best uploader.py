import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secrets.json'
VIDEO_FILE = 'video.mp4'

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=['https://www.googleapis.com/auth/youtube.upload']
)
credentials = flow.run_local_server(port=0)
youtube = build('youtube', 'v3', credentials=credentials)

body = {
    'snippet': {
        'title': 'Name',
        'description': 'Description',
        'categoryId': '22'  # people and blogs
    },
    'status': {
        'privacyStatus': 'unlisted'  # unlisted by default
    }
}

media = MediaFileUpload(
    VIDEO_FILE,
    chunksize=1024 * 1024 * 8,
    resumable=True
)

request = youtube.videos().insert(
    part=','.join(body.keys()),
    body=body,
    media_body=media
)

print("Starting video upload to YouTube...")

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Загружено: {int(status.progress() * 100)}%")

print("Success! The video has been completely uploaded to your channel")