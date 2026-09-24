# YouTube Data API v3 Automation Scripts

A collection of Python utility scripts for interacting with the **YouTube Data API v3**, designed for automated video uploading, metadata management, and dynamic title updates.

---

## Features & Scripts

| Script | Description |
| :--- | :--- |
| **`views.py`** | Runs a background loop that periodically fetches a video's stats and dynamically updates its title with the current view and like counts. (example: [click me](https://www.youtube.com/watch?v=Pr9PDr6WuTw)) |
| **`best uploader.py`** | Handles reliable, chunked (resumable) video uploads with customizable metadata (title, description, category, and privacy settings). |
| **`unique id.py`** | Automatically uploads a video file and immediately updates its title to match its newly assigned YouTube Video ID]. (example: [click me](https://www.youtube.com/watch?v=NFpIVSRa_PE)) |

## Authentication Files (`client_secrets.json` & `token.json`)

The project relies on two distinct configuration and credential files for OAuth 2.0 authorization. Both must be properly handled:

* **`client_secrets.json` (The Blueprint)**
  * **What it is:** The official client configuration file downloaded from the Google Cloud Console. It contains your app's public Client ID, Client Secret, and redirect URIs.
  * **Why it is needed:** It acts as the master key that identifies your application to Google's authorization servers, allowing the script to initiate the OAuth login flow.
  * **Why you might need it:** Required initially for every fresh setup or if you create a new Google Cloud project/credentials.

* **`token.json` (The Session State)**
  * **What it is:** An automatically generated file created locally in your project directory upon your first successful browser-based login. It securely stores your access and refresh tokens.
  * **Why it is needed:** It allows the scripts to authenticate silently in the background without constantly re-triggering the browser OAuth consent flow.
  * **Why you might need it:** Essential for automated or headless environments (such as remote servers, VPS, or scheduled cron tasks) where opening a web browser for manual authentication is impossible.

>  **Important Difference:** 
> * `client_secrets.json` defines *who the application is* (static file from Google Cloud).
> * `token.json` defines *your session authorization* (dynamic file generated after you log into your YouTube account). 
> 
> *Never commit either of these files to public version control (like GitHub).*
---

## Prerequisites & Setup

1. **Python 3.x** installed on your machine.
2. Install the required dependencies:
   ```bash
   pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 certifi
