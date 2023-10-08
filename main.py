# import os
# from dotenv import load_dotenv
# from ticket_master_utils import search_events, parse_event
# from spotify_utils import authenticate_to_spotify, rank_artists_by_song_count, get_all_liked_tracks
#
#
# def main():
#     load_dotenv()
#     ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
#     ticketmaster_api_url = os.getenv('TICKETMASTER_API_URL')
#
#     client_id = os.getenv('SPOTIFY_CLIENT_ID')
#     client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
#     redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
#     scope = os.getenv('SPOTIFY_APP_SCOPE')
#
#     sp_ = authenticate_to_spotify(client_id, client_secret, redirect_uri, scope)
#     top_artists = rank_artists_by_song_count(get_all_liked_tracks(sp_))
#
#     artists = []
#     for artist in top_artists:
#         if artist[1] >= 3:
#             artists.append(artist[0])
#
#     events_per_band = 7
#     for i in artists:
#         events = search_events(i, ticketmaster_api_key, ticketmaster_api_url, events_per_band)
#
#         if events:
#             for event in events:
#                 print(parse_event(band_name=i, event=event))
#                 print('_' * 200)
#
#
# if __name__ == '__main__':
#     main()