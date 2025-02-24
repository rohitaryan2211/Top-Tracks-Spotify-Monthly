# Spotify Top 50 Tracks Updater

This project updates a Spotify playlist with your top 50 tracks for the short term (Last 4 weeks) using the Spotify API and GitHub Actions.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Environment Variables](#environment-variables)
4. [GitHub Actions](#github-actions)
5. [Running Locally](#running-locally)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- **Spotify Account**: You need a Spotify account.
- **Spotify Developer Account**: Create a Spotify Developer account for a client ID and client secret.
- **GitHub Account**: You need a GitHub account for hosting and using GitHub Actions.

## Setup

### Step 1: Create a Spotify Developer App

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create an app and note down the **Client ID** and **Client Secret**.

### Step 2: Create a Spotify Playlist

1. Open Spotify and create a new playlist.
2. Note down the **Playlist ID** from the playlist URL.

### Step 3: Obtain a Refresh Token

1. Run `refresh_token.py` to get a refresh token.
2. Authenticate via a web browser.
3. The script will print the refresh token.

### Step 4: Create a `.env` File

Create a `.env` file with:

    client_id=YOUR_CLIENT_ID
    client_secret=YOUR_CLIENT_SECRET
    refresh_access_token=YOUR_REFRESH_TOKEN
    top50_tracks_short_id=YOUR_PLAYLIST_ID


Replace `YOUR_CLIENT_ID`, `YOUR_CLIENT_SECRET`, `YOUR_REFRESH_TOKEN`, and `YOUR_PLAYLIST_ID` with your actual values.

### Step 5: Create a `requirements.txt` File

Create a `requirements.txt` file with:

    python-dotenv==1.0.1
    Requests==2.32.3
    spotipy==2.23.0


## Environment Variables

For GitHub Actions, store environment variables as secrets:

1. Go to your GitHub repository settings.
2. Navigate to **Actions** > **Secrets**.
3. Add secrets:
   - `CLIENT_ID`
   - `CLIENT_SECRET`
   - `REFRESH_ACCESS_TOKEN`
   - `TOP50_TRACKS_SHORT_ID`

## GitHub Actions

The `actions.yml` file runs the script daily. Ensure your repository has the necessary permissions and secrets.

## Running Locally

1. Install dependencies using `pip install -r requirements.txt`.
2. Run the script using `python main.py`.

## Troubleshooting

- Ensure all environment variables are correctly set.
- Check the Spotify API status.
- Verify your GitHub Actions workflow configuration.

---

This project automates updating your Spotify playlist with your top tracks. Feel free to modify it as needed.
