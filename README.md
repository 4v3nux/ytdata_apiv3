# YouTube Data API v3 Automation Scripts

A collection of Python utility scripts for interacting with the **YouTube Data API v3**, designed for automated video uploading, metadata management, and dynamic title updates[cite: 1, 2, 3].

---

## Features & Scripts

| Script | Description |
| :--- | :--- |
| **`views.py`** | Runs a background loop that periodically fetches a video's stats and dynamically updates its title with the current view and like counts[cite: 1]. |
| **`best uploader.py`** | Handles reliable, chunked (resumable) video uploads with customizable metadata (title, description, category, and privacy settings)[cite: 2]. |
| **`unique id.py`** | Automatically uploads a video file and immediately updates its title to match its newly assigned YouTube Video ID[cite: 3]. |

---

## Prerequisites & Setup

1. **Python 3.x** installed on your machine.
2. Install the required dependencies:
   ```bash
   pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 certifi
