import os
from dotenv import load_dotenv
from ticket_master_utils import search_events, parse_event
from spotify_utils import get_artists_sorted_by_liked_tracks, authenticate_to_spotify


def format_events(events):
    formatted_events = []
    for event in events:
        formatted_event = {
            'Event Name': event['name'],
            'Date and Time': event['date_and_time'],
            'Event URL': event['event_url']
        }
        formatted_events.append(formatted_event)
    return formatted_events


def main():
    load_dotenv()
    ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
    ticketmaster_api_url = os.getenv('TICKETMASTER_API_URL')

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    scope = os.getenv('SPOTIFY_SCOPE')

    sp_ = authenticate_to_spotify(client_id, client_secret, redirect_uri, scope)

    followed_artists_sorted = get_artists_sorted_by_liked_tracks(sp_)

    for artist in followed_artists_sorted:
        artist_events = []

        events = search_events(artist, ticketmaster_api_key, ticketmaster_api_url)
        for event in events:
            event_info = parse_event(event)
            artist_events.append(event_info)

        formatted_events = format_events(artist_events)
        all_events.append(formatted_events)



if __name__ == '__main__':
    main()