import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID= os.getenv('client_id')
CLIENT_ID_SECRET = os.getenv('client_secret')
TOP50_TRACKS_SHORT_ID = os.getenv('top50_tracks_short_id')
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

    sp.user_playlist_replace_tracks(user=user_info, playlist_id=f'{TOP50_TRACKS_SHORT_ID}', tracks=list())
    
    sp.user_playlist_replace_tracks(user=user_info, playlist_id=f'{TOP50_TRACKS_SHORT_ID}', tracks=list(top50playlist_short.values()))
        
    print('Script Executed Successfully')

if __name__ == '__main__':
    main()

