import os

import spotipy
from dotenv import load_dotenv
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_caching import Cache
from spotipy.oauth2 import SpotifyOAuth
from utils.spotify_utils import (get_all_liked_tracks,
                                 get_current_user_top_artists,
                                 rank_artists_by_song_count)
from utils.ticket_master_utils import parse_event, search_events

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["SESSION_COOKIE_NAME"] = "spotify-auth"

# Configure cache
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = "user-top-read user-library-read user-follow-read"

# Ticketmaster configuration
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
TICKETMASTER_API_URL = os.getenv("TICKETMASTER_API_URL")


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE,
    )


@app.template_filter("datetime_format")
def datetime_format(value, date_format="%b %d"):
    try:
        return value.strftime(date_format)
    except AttributeError:
        return "Date unknown"


@app.route("/")
def index():
    return render_template("index.html", logged_in="spotify_token" in session)


@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


@app.route("/login")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/logout")
def logout():
    session.pop("spotify_token", None)
    cache.clear()
    return redirect(url_for("index"))


@app.route("/callback")
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(
        code=code, as_dict=True
    )  # need to change this to false and fix error
    session["spotify_token"] = token_info
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@cache.cached(timeout=3600, query_string=True)
def dashboard():
    if "spotify_token" not in session:
        return redirect(url_for("login"))

    token_info = session.get("spotify_token")
    sp_oauth = create_spotify_oauth()

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["spotify_token"] = token_info

    sp = spotipy.Spotify(auth=token_info["access_token"])

    try:
        # Validate inputs
        num_artists = min(max(int(request.args.get("num_artists", 10)), 1), 50)
        events_per_artist = min(
            max(int(request.args.get("events_per_artist", 5)), 1), 20
        )

        # Get artists
        top_artists = get_current_user_top_artists(sp, limit=num_artists)[:num_artists]

        # Get ranked artists
        @cache.memoize(timeout=3600)
        def get_cached_data():
            liked_tracks = get_all_liked_tracks(sp)
            return rank_artists_by_song_count(liked_tracks)[:num_artists]

        ranked_artists = get_cached_data()

        # Get events
        events = []
        for artist in top_artists:
            artist_events = search_events(
                artist_name=artist,
                ticketmaster_api_key=TICKETMASTER_API_KEY,
                ticketmaster_api_url=TICKETMASTER_API_URL,
                events_to_get=events_per_artist,
                start_date=None,
                end_date=None,
            )
            if artist_events:
                events.extend([parse_event(artist, event) for event in artist_events])

        return render_template(
            "dashboard.html",
            top_artists=top_artists,
            ranked_artists=ranked_artists,
            events=events,
            num_artists=num_artists,
            events_per_artist=events_per_artist,
        )

    except Exception:
        return redirect(url_for("logout"))


if __name__ == "__main__":
    app.run(debug=True)
