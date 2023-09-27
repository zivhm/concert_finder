import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv


# def search_events(artist_name, ticketmaster_api_key, ticketmaster_api_url, size=10):
#     ticketmaster_params = {
#         'apikey': ticketmaster_api_key,
#         'keyword': artist_name,
#         'size': size  # Specify the number of events to fetch
#     }
#     ticketmaster_response = requests.get(ticketmaster_api_url, params=ticketmaster_params)
#
#     upcoming_events = []
#
#     if ticketmaster_response.status_code == 200:
#         ticketmaster_data = ticketmaster_response.json()
#         for event in ticketmaster_data.get('_embedded', {}).get('events', []):
#             upcoming_events.append(event)
#     else:
#         print(f'Error: {ticketmaster_response.status_code}')
#
#     return upcoming_events


def search_events(artist_name, ticketmaster_api_key, ticketmaster_api_url, size=10):
    # Calculate the date range for the next 7 days
    today = datetime.now()
    end_date = today + timedelta(days=7)

    # Format the date strings as required by Ticketmaster API
    start_date_str = today.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    ticketmaster_params = {
        'apikey': ticketmaster_api_key,
        'keyword': artist_name,
        'size': size,
        'startDateTime': start_date_str,
        'endDateTime': end_date_str
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


def parse_event(event):
    name = event['name']

    # Check if the 'dates' key exists
    if 'dates' in event:
        if 'start' in event['dates'] and 'localDate' in event['dates']['start']:
            local_date = event['dates']['start']['localDate']
        else:
            local_date = "Unknown"

        if 'start' in event['dates'] and 'localTime' in event['dates']['start']:
            local_time = event['dates']['start']['localTime']
        else:
            local_time = "Unknown"

        # Check if the 'timezone' key exists in the 'dates' dictionary
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
        formatted_datetime = event_datetime.strftime('%A, %B %d, %Y at %I:%M %p')

    # Check if the '_embedded' key exists
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
        "name": name,
        "date_and_time": f"{local_date} {local_time} ({timezone})",
        "start_datetime": formatted_datetime,
        "event_url": event.get('url', "URL not available"),
        "timezone": timezone,
        "locale": event.get('locale', "Locale not available"),
        "venue_name": venue_name,
        "venue_address": venue_address
    }

    return event_info


if __name__ == '__main__':
    load_dotenv()

    TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
    TICKETMASTER_API_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'

    artists = ['The Devil Wears Prada']
    artist_events = {}
    events_to_get = 10
    events = search_events(artists[0], TICKETMASTER_API_KEY, TICKETMASTER_API_URL, events_to_get)
    print(len(events))

