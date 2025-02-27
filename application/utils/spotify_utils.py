import spotipy
from tqdm import tqdm
import time

def authenticate_to_spotify(client_id, client_secret, redirect_uri, scope):
    """Return a Spotipy client with valid auth."""

    auth_manager = spotipy.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def get_followed_artists(sp, limit=50):
    """Returns a list of the user's followed artists."""

    followed_artists = []
    num_requests = (limit + 49) // 50
    after_name = None

    for i in range(num_requests):
        if i == num_requests - 1:
            final_limit = limit % 50 if limit % 50 != 0 else 50
            results = sp.current_user_followed_artists(limit=final_limit, after=after_name)
        else:
            results = sp.current_user_followed_artists(limit=50, after=after_name)

        for x in results['artists']['items']:
            followed_artists.append(x['name'])

        if 'next' in results['artists']:
            after_name = results['artists']['cursors']['after']
        else:
            break

    return followed_artists


def get_current_user_top_artists(sp, limit=100, time_range='long_term'):
    """Returns a list of the user's top artists."""

    top_artists = []
    num_requests = (limit + 49) // 50
    offset = 0

    for i in range(num_requests):
        if i == num_requests - 1:
            final_limit = limit % 50 if limit % 50 != 0 else 50
            results = sp.current_user_top_artists(limit=final_limit, offset=offset, time_range=time_range)
        else:
            results = sp.current_user_top_artists(limit=50, offset=offset, time_range=time_range)

        offset = (offset + 50)
        for x in results['items']:
            top_artists.append(x['name'])

    return top_artists


def get_current_user_top_tracks(sp, limit=50):
    """returns a list of tuples (track_id, track_name)"""

    top_tracks = []
    num_requests = (limit + 49) // 50
    offset = 0

    for i in range(num_requests):
        if i == num_requests - 1:
            final_limit = limit % 50 if limit % 50 != 0 else 50
            results = sp.current_user_top_tracks(limit=final_limit, offset=offset)
        else:
            results = sp.current_user_top_tracks(limit=50, offset=offset)

        offset = (offset + 50)
        for x in results['items']:
            top_tracks.append((x['name'], x['artists'][0]['name']))

    return top_tracks


def get_liked_tracks(sp, limit=50):
    """returns a list of tuples (track_id, track_name)"""

    liked_tracks = []
    num_requests = (limit + 49) // 50
    offset = 0

    for i in range(num_requests):
        if i == num_requests - 1:
            final_limit = limit % 50 if limit % 50 != 0 else 50
            results = sp.current_user_saved_tracks(limit=final_limit, offset=offset)
        else:
            results = sp.current_user_saved_tracks(limit=50, offset=offset)

        offset = (offset + 50)
        for x in results['items']:
            liked_tracks.append((x['track']['name'], x['track']['artists'][0]['name']))

    return liked_tracks


def get_all_liked_tracks(sp):
    """Cached version of liked tracks fetcher"""
    liked_tracks = []
    offset = 0
    limit = 50
    
    total_tracks = sp.current_user_saved_tracks(limit=1)['total']
    num_requests = (total_tracks + limit - 1) // limit
    
    for _ in range(num_requests):
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        liked_tracks.extend([
            (item['track']['name'], item['track']['artists'][0]['name'] if item['track']['artists'] else "Unknown Artist")
            for item in results['items']
        ])
        offset += limit
        

        time.sleep(0.1)  # 100ms delay between requests
        
    return liked_tracks


def rank_artists_by_song_count(liked_tracks):
    """
    Takes a list of tuples (track_name, track_artist) of liked tracks,
    and outputs a list of tuples (artist, song_count) ranked by song_count.
    """

    artist_count = {}

    for track in liked_tracks:
        artist = track[1]
        if artist not in artist_count:
            artist_count[artist] = 0

        artist_count[artist] += 1

    ranked_artists = sorted(artist_count.items(), key=lambda item: item[1], reverse=True)

    return ranked_artists


if __name__ == "__main__":
    ...
