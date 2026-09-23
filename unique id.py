import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

def upload_and_rename_to_youtube_id(video_file_path):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    print("Step 1: Uploading video to YouTube...")
    body_insert = {
        "snippet": {
            "title": "Name", 
            "description": "Description",
            "categoryId": "22"   # people and blogs
        },
        "status": {
            "privacyStatus": "unlisted"  # unlisted by default
        }
    }

    media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body_insert,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response['id']
    print(f"\nVideo uploaded! YouTube assigned it the ID:: {video_id}")
    print("Step 2: Changing the video title to its ID...")
    
    video_resource = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    snippet = video_resource["items"][0]["snippet"]
    snippet["title"] = video_id

    update_request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": snippet
        }
    )
    update_response = update_request.execute()

    print("\nDone! Video title successfully changed to its ID.")
    print(f"Final title: {update_response['snippet']['title']}")
    print(f"Video link: https://youtu.be/{video_id}")

if __name__ == "__main__":
    file_path = input("Enter the path to the video file (e.g., video.mp4): ").strip()
    
    if os.path.exists(file_path):
        upload_and_rename_to_youtube_id(file_path)
    else:
        print("Error: The specified file was not found!")