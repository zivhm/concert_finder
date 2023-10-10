# import os
import requests
from dotenv import load_dotenv
from datetime import datetime


# def search_events(artist_name, ticketmaster_api_key, ticketmaster_api_url, size=10):
#     ticketmaster_params = {
#         'apikey': ticketmaster_api_key,
#         'keyword': artist_name,
#         'size': size
#     }

#     ticketmaster_response = requests.get(ticketmaster_api_url, params=ticketmaster_params)

#     upcoming_events = []

#     if ticketmaster_response.status_code == 200:
#         ticketmaster_data = ticketmaster_response.json()
#         for event in ticketmaster_data.get('_embedded', {}).get('events', []):
#             upcoming_events.append(event)
#     else:
#         print(f'Error: {ticketmaster_response.status_code}')

#     if len(upcoming_events) == 0:
#         return None

#     return upcoming_events


def search_events(artist_name, ticketmaster_api_key, ticketmaster_api_url, start_date, end_date, events_to_get=10):
    ticketmaster_params = {
        'apikey': ticketmaster_api_key,
        'keyword': artist_name,
        'startDateTime': start_date,  # Specify the start date
        'endDateTime': end_date,      # Specify the end date
        'size': events_to_get
    }

    ticketmaster_response = requests.get(ticketmaster_api_url, params=ticketmaster_params)

    upcoming_events = []

    if ticketmaster_response.status_code == 200:
        ticketmaster_data = ticketmaster_response.json()
        for event in ticketmaster_data.get('_embedded', {}).get('events', []):
            upcoming_events.append(event)
    else:
        print(f'Error: {ticketmaster_response.status_code}')

    if len(upcoming_events) == 0:
        return None

    return upcoming_events


def group_events_by_artist(events):
    artist_events = defaultdict(list)
    for event in events:
        artist_name = event['band_name'].lower()
        artist_events[artist_name].append(event)

    artist_events_dict = dict(artist_events)

    return artist_events_dict


def parse_event(band_name, event):
    band_name = band_name
    event_name = event['name']

    if 'dates' in event:
        if 'start' in event['dates'] and 'localDate' in event['dates']['start']:
            local_date = event['dates']['start']['localDate']
        else:
            local_date = "Unknown"

        if 'start' in event['dates'] and 'localTime' in event['dates']['start']:
            local_time = event['dates']['start']['localTime']
        else:
            local_time = "Unknown"

        if 'timezone' in event['dates']:
            timezone = event['dates']['timezone']
        else:
            timezone = "Unknown"
    
    else:
        local_date = "Unknown"
        local_time = "Unknown"
        timezone = "Unknown"

    if local_date == "Unknown" or local_time == "Unknown":
        event_datetime = None
        formatted_datetime = "Date and time unknown"
    else:
        event_datetime = datetime.strptime(f"{local_date} {local_time}", '%Y-%m-%d %H:%M:%S')
        formatted_datetime = event_datetime.strftime('%A, %B %d, %Y at %I:%M %p')\

    if 'images' in event:
        image_url = event['images'][-1].get('url', "Image not available")
    else:
        image_url = "Image not available"

    if '_embedded' in event and 'venues' in event['_embedded']:
        if event['_embedded']['venues']:
            venue_name = event['_embedded']['venues'][0].get('name', "Venue name not available")
            venue_address = event['_embedded']['venues'][0].get('address', {}).get('line1', "Venue address not available")
        else:
            venue_name = "Venue information not available"
            venue_address = "Venue information not available"

    else:
        venue_name = "Venue information not available"
        venue_address = "Venue information not available"

    event_info = {
        "band_name": band_name,
        "event_name": event_name,
        "date_and_time": f"{local_date} {local_time} ({timezone})",
        "start_datetime": formatted_datetime,
        "event_url": event.get('url', "URL not available"),
        "timezone": timezone,
        "locale": event.get('locale', "Locale not available"),
        "venue_name": venue_name,
        "venue_address": venue_address,
        "image": image_url
    }

    return event_info


if __name__ == '__main__':
    ...
    # load_dotenv()
    #
    # TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
    # TICKETMASTER_API_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'
    #
    # artists = ['Lorna Shore', 'The devil wears prada', 'gojira', 'thy art is murder', 'igorrr', 'bring me the horizon']
    #
    # events_to_get = 3
    # for i in artists:
    #     events = search_events(i, TICKETMASTER_API_KEY, TICKETMASTER_API_URL, events_to_get)
    #
    #     if events:
    #         for event in events:
    #             print(parse_event(band_name=i, event=event))
    #             print('_' * 200)
    #
