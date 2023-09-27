import os
from dotenv import load_dotenv
from ticket_master_utils import search_events, parse_event
from spotify_utils import get_artists_sorted_by_liked_tracks, authenticate_to_spotify

def main():
    load_dotenv()
    ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
    ticketmaster_api_url = os.getenv('TICKETMASTER_API_URL')

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    scope = os.getenv('SPOTIFY_SCOPE')

    sp_ = authenticate_to_spotify(client_id, client_secret, redirect_uri, scope)

    limit = 30

    followed_artists_sorted = get_artists_sorted_by_liked_tracks(sp_, limit=limit)
    all_events = []
    for artist in followed_artists_sorted:
        print(artist)
        events = search_events(artist, ticketmaster_api_key, ticketmaster_api_url)
        if events is None:
            pass

        else:
            for event in events:
                event_info = parse_event(event)
                all_events.append(event_info)

    for i in all_events:
        print(i.get('name'))
    #
if __name__ == '__main__':
    main()