import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
from dotenv import load_dotenv
import os

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

    playlist_name = 'Top Tracks Per Month'
    playlist_archive_name = 'Top Tracks Archive'

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

    for playlist in playlists:
        if playlist["name"] == playlist_archive_name:
            playlist_archive_id = playlist["id"]
            break

    archive_tracks = []
    offset = 0

    while True:
        response = sp.playlist_tracks(playlist_archive_id, offset=offset, limit=50)
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
        sp.user_playlist_add_tracks(user=user_info, playlist_id=playlist_archive_id, tracks=new_archive_tracks, position=0)
        print(f"Added {len(new_archive_tracks)} new tracks to the playlist: {playlist_archive_name}")
    else:
        print("No new tracks to add to the archive playlist.")

    print('Script Executed Successfully')

if __name__ == '__main__':
    main()

