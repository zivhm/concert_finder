import os
import streamlit as st
from dotenv import load_dotenv
from ticket_master_utils import search_events, parse_event
from spotify_utils import authenticate_to_spotify, get_current_user_top_artists
from streamlit_card import card
from collections import defaultdict


def group_events_by_artist(events):
    artist_events = defaultdict(list)
    for event in events:
        artist_name = event['band_name'].lower()
        artist_events[artist_name].append(event)

    artist_events_dict = dict(artist_events)

    return artist_events_dict

def beutify_event(event):
    with st.expander("Event Details", expanded=False):
        st.title("Concert Details")

        st.header(event["band_name"])
        st.subheader(event["event_name"])
        st.write(f"Date and Time: {event['start_datetime']} ({event['timezone']})")
        st.write(f"Venue: {event['venue_name']}")
        st.write(f"Address: {event['venue_address']}")
        st.write(f"Event URL: [{event['event_name']}]({event['event_url']})")
    

load_dotenv()
ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
ticketmaster_api_url = os.getenv('TICKETMASTER_API_URL')

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
scope = os.getenv('SPOTIFY_APP_SCOPE')


st.title('Content Finder')

sp = None

st.markdown(body='Please connect to your Spotify account')
sp_connect_button = st.button(label='Connect', key='connect_spotify_button')
events_to_get = st.slider(min_value=1, max_value=10, value=1, step=1, label='events_to_get')

all_artists = []
if sp_connect_button:
    try:
        sp = authenticate_to_spotify(client_id, client_secret, redirect_uri, scope)
    
    except Exception as e:
        st.error(e)
    
    finally:
        top_artists = get_current_user_top_artists(sp, limit=500)

        for artist in top_artists:
            artist_events = []
            events = search_events(artist, ticketmaster_api_key, ticketmaster_api_url, events_to_get)
        
            if events:
                for event in events:
                    if event:
                            event = parse_event(band_name=artist, event=event)
                            artist_events.append(event)

                all_artists.append(artist_events)

                for artist_ev in all_artists:
                    band = artist_ev[0]['band_name']
                    st.text(band)
                    x = 0
                    for event in artist_ev:
                        with st.expander(f"{band}", expanded=False):
                            text = [f'Band: {event["band_name"]}', f'Event: {event["event_name"]}', f'Date and Time: {event["date_and_time"]}', f'Venue: {event["venue_name"]}', f'Address: {event["venue_address"]}']

                            card(title=event["event_name"],
                                    text= text,
                                    url=f"{event['event_url']}",
                                    styles= {
                                        "card": {
                                            "width": "700px",
                                            "height": "450px"
                                            }
                                        },
                                    image=event["image"], 
                                    key=(f'{event["band_name"]}+{x}'),
                                    )
                            x += 1

                        