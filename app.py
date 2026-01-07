import sqlite3
from flask import Flask, request, render_template, session, redirect
from flask_session import Session

app = Flask(__name__)

# configures sessions for the user
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#function to connect to database
def get_db_connection():
    conn = sqlite3.connect('songs.db')
    conn.row_factory = sqlite3.Row 
    return conn

#function to get songs according to each metric
def get_mood_songs(energy, valence):
    with get_db_connection() as db:
        return db.execute("""SELECT * FROM (
            SELECT track_id, track_name, track_artist, track_popularity
            FROM songs WHERE valence BETWEEN ? AND ?
            AND energy BETWEEN ? AND ?
            ORDER BY RANDOM()
            LIMIT 100
            )
            ORDER BY track_popularity DESC
            LIMIT 30;""",
            (valence[0], valence[1], energy[0], energy[1])
        ).fetchall()
    
# default route, loads home page
@app.route("/")
def index():
    return render_template("index.html")

# route when user mood is happy
@app.route("/happy")
def happy():
    happySongs = get_mood_songs((0.60, 0.90), (0.70, 1.00))
    happy = "happy"
    return render_template("mood.html", mood=happySongs, type=happy)

# route when user mood is sad
@app.route("/sad")
def sad():
    sadSongs = get_mood_songs((0.00, 0.40), (0.00, 0.30))
    sad = "sad"
    return render_template("mood.html", mood=sadSongs, type=sad)

# route when user mood is energetic
@app.route("/energetic")
def energetic():
    energeticSongs = get_mood_songs((0.80, 0.90), (0.40, 1.00))
    energetic = "energetic"
    return render_template("mood.html", mood=energeticSongs, type=energetic)

# route when user mood is chill
@app.route("/chill")
def chill():
    chillSongs = get_mood_songs((0.20, 0.50), (0.40, 0.70))
    chill = "chill"
    return render_template("mood.html", mood=chillSongs, type=chill)

# route when user wants to go to the favorites route
@app.route("/favorites", methods=["GET", "POST"])
def favorites():
    db = get_db_connection()

    if "favorites" not in session:
        session["favorites"] = []
        #creates a new session for first time users

    if request.method == "POST":
        if request.form.get("song_id"):
            #condition to see if user wants to add to favorites
            song_id = request.form.get("song_id")

            favorites = set(session["favorites"])
            favorites.add(song_id)

            session["favorites"] = list(favorites)
            session.modified = True

        elif request.form.get("clear"):
            #condition to see if user wants to clear songs
            session["favorites"] = []
            session.modified = True
            return redirect("/favorites")

        return "", 204

    if len(session["favorites"]) == 0:
        # condition allows to create the table in the favorites page
        songs = []

    else:
        # condition to display favorites in a table
        placeholders = ",".join(["?"] * len(session["favorites"]))
        query = f"""SELECT track_id, track_name, track_artist, track_popularity, 
                    track_album_name, track_album_release_date 
                    FROM songs WHERE track_id IN ({placeholders})"""
        songs = db.execute(query, session["favorites"]).fetchall()

    db.close()
    return render_template("favorites.html", songs=songs)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
