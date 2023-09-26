import os
import requests
from datetime import datetime
from dotenv import load_dotenv


import requests


def search_events(artist_name, ticketmaster_api_key, ticketmaster_api_url, size=10):
    ticketmaster_params = {
        'apikey': ticketmaster_api_key,
        'keyword': artist_name,
        'size': size  # Specify the number of events to fetch
    }
    ticketmaster_response = requests.get(ticketmaster_api_url, params=ticketmaster_params)

    upcoming_events = []

    if ticketmaster_response.status_code == 200:
        ticketmaster_data = ticketmaster_response.json()
        for event in ticketmaster_data.get('_embedded', {}).get('events', []):
            upcoming_events.append(event)
    else:
        print(f'Error: {ticketmaster_response.status_code}')

    return upcoming_events



def parse_event(event):
    name = event['name']

    try:
        local_date = event['dates']['start']['localDate']
        local_time = event['dates']['start']['localTime']
        timezone = event['dates']['timezone']
    except KeyError:
        local_date = "Unknown"
        local_time = "Unknown"
        timezone = "Unknown"

    event_datetime = datetime.strptime(f"{local_date} {local_time}", '%Y-%m-%d %H:%M:%S')
    formatted_datetime = event_datetime.strftime('%A, %B %d, %Y at %I:%M %p')

    venue_name = event['_embedded']['venues'][0]['name']
    venue_address = event['_embedded']['venues'][0]['address']['line1']

    event_info = {
        "name": name,
        "date_and_time": f"{local_date} {local_time} ({timezone})",
        "start_datetime": formatted_datetime,
        "event_url": event['url'],
        "timezone": timezone,
        "locale": event['locale'],
        "venue_name": venue_name,
        "venue_address": venue_address
    }

    return event_info


if __name__ == '__main__':
    load_dotenv()

    EVENTBRITE_API_KEY = os.getenv('EVENTBRITE_API_KEY')
    EVENTBRITE_API_URL = 'https://www.eventbriteapi.com/v3/events/search/'

    TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
    TICKETMASTER_API_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'

    artists = ['The Devil Wears Prada']
    artist_events = {}
    events_to_get = 10
    events = search_events(artists[0], TICKETMASTER_API_KEY, TICKETMASTER_API_URL, events_to_get)
    print(len(events))

