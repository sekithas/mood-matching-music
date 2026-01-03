import sqlite3
from flask import Flask, request, render_template, session, redirect
from flask_session import Session

app = Flask(__name__)

# configures sessions for the user
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = sqlite3.connect('songs.db')
    conn.row_factory = sqlite3.Row # Allows name-based access to columns
    return conn

# default route, loads home page
@app.route("/")
def index():
    return render_template("index.html")

# route when user mood is happy
@app.route("/happy")
def happy():
    db = get_db_connection()
    happySongs = db.execute("SELECT track_id, track_name, track_artist, track_popularity FROM songs WHERE ((valence >= 0.70 AND valence <= 1.00) AND (energy >= 0.60 AND energy <= 0.90)) ORDER BY RANDOM() LIMIT 30").fetchall()
    db.close()
    happy = "happy"
    return render_template("mood.html", mood=happySongs, type=happy)

# route when user mood is sad
@app.route("/sad")
def sad():
    db = get_db_connection()
    sadSongs = db.execute("SELECT track_id, track_name, track_artist, track_popularity FROM songs WHERE ((valence >= 0.00 AND valence <= 0.30) AND (energy >= 0.00 AND energy <= 0.40)) ORDER BY RANDOM() LIMIT 30").fetchall()
    db.close()
    sad = "sad"
    return render_template("mood.html", mood=sadSongs, type=sad)

# route when user mood is energetic
@app.route("/energetic")
def energetic():
    db = get_db_connection()
    energeticSongs = db.execute(
        "SELECT track_id, track_name, track_artist, track_popularity FROM songs WHERE ((valence >= 0.40 AND valence <= 1.00) AND (energy >= 0.80 AND energy <= 0.90)) ORDER BY RANDOM() LIMIT 30").fetchall()
    db.close()
    energetic = "energetic"
    return render_template("mood.html", mood=energeticSongs, type=energetic)

# route when user mood is chill
@app.route("/chill")
def chill():
    db = get_db_connection()
    chillSongs = db.execute("SELECT track_id, track_name, track_artist, track_popularity FROM songs WHERE ((valence >= 0.40 AND valence <= 0.70) AND (energy >= 0.20 AND energy <= 0.50)) ORDER BY RANDOM() LIMIT 30").fetchall()
    db.close()
    chill = "chill"
    return render_template("mood.html", mood=chillSongs, type=chill)

# route when user wants to go to the favorites route
@app.route("/favorites", methods=["GET", "POST"])
def favorites():
    db = get_db_connection()
    # if user first time logs in, then a new session list is formed, to keep track of the favorite songs
    if "favorites" not in session:
        session["favorites"] = []

    # user wants input, either to clear songs from favorites or add to favorites
    if request.method == "POST":
        # checks if user wants to add a song
        if request.form.get("song_id"):
            song_id = request.form.get("song_id")

            favorites = set(session["favorites"])
            #ensures no duplicates so user can't add same song twice to favorites
            favorites.add(song_id)

            session["favorites"] = list(favorites)
            session.modified = True

        # checks if user wants to clear their favorites
        elif request.form.get("clear"):
            session["favorites"] = []
            session.modified = True
            #clears the current favorite songs when user clicks "Clear Favorites"

        # returns the favorites route to their favorites page either way
        db.close()
        return redirect("/favorites")

    # if user has no favorites currently, then a list is created
    if len(session["favorites"]) == 0:
        songs = []
    # allows to create the table in the favorites page
    else:
        # creates (?, ?, ? ...) as SQL cannot read python list itself
        placeholders = ",".join(["?"] * len(session["favorites"]))
        query = f"SELECT track_id, track_name, track_artist, track_popularity, track_album_name, track_album_release_date FROM songs WHERE track_id IN ({placeholders})"
        # adds details of each song as a dictionary to the songs list
        songs = db.execute(query, session["favorites"]).fetchall()
    db.close()
    return render_template("favorites.html", songs=songs)

#prevent the same song being added to favorites twice, by preventing route execution twice
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
