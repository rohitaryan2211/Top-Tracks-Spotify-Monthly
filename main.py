import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

CLIENT_ID= os.getenv('client_id')
CLIENT_ID_SECRET = os.getenv('client_secret')
REFRESH_ACCESS_TOKEN = os.getenv('refresh_access_token')

def get_user_id(sp):
    return sp.me()["id"]

def get_top50tracks_short(sp):
    top50playlist_short = {}
    try:
        results = sp.current_user_top_tracks(limit=50, offset=0, time_range='short_term')
        for idx, item in enumerate(results['items']):
           top50playlist_short[item['name']]=item['uri']

    except:
        print("An error occured")

    return top50playlist_short

# Function to refresh access token
def refresh_access_token(refresh_token):
    
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    auth_header = {'Authorization': 'Basic ' + base64.b64encode((f'{CLIENT_ID}' + ':' + f'{CLIENT_ID_SECRET}').encode()).decode()}
    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=auth_header)
    return response.json().get('access_token')

def main():

    print("Script started")

    new_access_token = refresh_access_token(f'{REFRESH_ACCESS_TOKEN}')

    sp = spotipy.Spotify(auth=new_access_token)
        
    top50playlist_short = get_top50tracks_short(sp)

    user_info = get_user_id(sp)

    current_date = datetime.now()
    month_year = current_date.strftime("%B %Y") 

    playlist_name = 'Top Tracks Per Month'
    archive_playlist_name = f'Top Tracks Archive {month_year}'

    playlists = []
    offset = 0

    while True:
        batch = sp.current_user_playlists(limit=50, offset=offset)["items"]
        if not batch:
            break
        playlists.extend(batch)
        offset += 50
    
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            break

    archive_playlist_exists = False
    archive_playlist_id = None
    
    for playlist in playlists:
        if playlist["name"] == archive_playlist_name:
            archive_playlist_id = playlist["id"]
            archive_playlist_exists = True
            break

    if not archive_playlist_exists:
        new_playlist = sp.user_playlist_create(
            user=user_info,
            name=archive_playlist_name,
            public=True,
            description=f"Auto-generated archive of Top Tracks Per Month for {month_year}"
        )
        archive_playlist_id = new_playlist["id"]
        print(f"Created new playlist: {archive_playlist_name}")
    else:
        print(f"Playlist already exists: {archive_playlist_name}")

    archive_tracks = []
    offset = 0

    while True:
        response = sp.playlist_tracks(archive_playlist_id, offset=offset, limit=50)
        items = response['items']
        if not items:
            break
        for item in items:
            track = item['track']
            if track:  
                archive_tracks.append(track['id']) 
        offset += 50

    for i in range(len(archive_tracks)):
        archive_tracks[i] = 'spotify:track:'+ archive_tracks[i]

    new_archive_tracks = []

    for i in range(len(list(top50playlist_short.values()))):
        if list(top50playlist_short.values())[i] not in archive_tracks:
            new_archive_tracks.append(list(top50playlist_short.values())[i])

    sp.user_playlist_replace_tracks(user=user_info, playlist_id=playlist_id, tracks=list())
    sp.user_playlist_replace_tracks(user=user_info, playlist_id=playlist_id, tracks=list(top50playlist_short.values()))
    print(f"Updated the playlist: {playlist_name}")

    if len(new_archive_tracks) > 0:
        sp.user_playlist_add_tracks(user=user_info, playlist_id=archive_playlist_id, tracks=new_archive_tracks, position=0)
        print(f"Added {len(new_archive_tracks)} new tracks to the playlist: {archive_playlist_name}")
    else:
        print("No new tracks to add to the archive playlist.")

    print('Script Executed Successfully')

if __name__ == '__main__':
    main()

