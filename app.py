import sqlite3
from flask import Flask, request, render_template, session, redirect, jsonify
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
def get_mood_songs(energy, valence, search=None):
    query = """
        SELECT * FROM (SELECT DISTINCT track_id, track_name, track_artist, track_popularity
        FROM songs
        WHERE valence BETWEEN ? AND ?
        AND energy BETWEEN ? AND ?
        """
    params = [valence[0], valence[1], energy[0], energy[1]]

    if search:
        query += " AND (track_name LIKE ? OR track_artist LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += """
        ORDER BY RANDOM()
        LIMIT 100)
        sub
        ORDER BY track_popularity DESC
        LIMIT 30;
        """

    with get_db_connection() as db:
        return db.execute(query, params).fetchall()
    
# default route, loads home page
@app.route("/")
def index():
    return render_template("index.html")


# live search route
@app.route("/search/<mood>")
def search_mood(mood):
    search_text = request.args.get("q", "").strip()

    mood_ranges = {
        "happy": ((0.60, 0.90), (0.70, 1.00)),
        "sad": ((0.00, 0.40), (0.00, 0.30)),
        "energetic": ((0.80, 0.90), (0.40, 1.00)),
        "chill": ((0.20, 0.50), (0.40, 0.70))
    }

    if mood not in mood_ranges:
        return jsonify([])

    energy, valence = mood_ranges[mood]
    songs = get_mood_songs(energy, valence, search=search_text)

    results = [
        {
            "track_id": s["track_id"],
            "track_name": s["track_name"],
            "track_artist": s["track_artist"],
            "track_popularity": s["track_popularity"]
        } for s in songs
    ]

    return jsonify(results)

# route when user mood is happy
@app.route("/happy")
def happy():
    happySongs = get_mood_songs((0.60, 0.90), (0.70, 1.00), request.args.get("search"))
    happy = "happy"
    return render_template("mood.html", mood=happySongs, type=happy)

# route when user mood is sad
@app.route("/sad")
def sad():
    sadSongs = get_mood_songs((0.00, 0.40), (0.00, 0.30), request.args.get("search"))
    sad = "sad"
    return render_template("mood.html", mood=sadSongs, type=sad)

# route when user mood is energetic
@app.route("/energetic")
def energetic():
    energeticSongs = get_mood_songs((0.80, 0.90), (0.40, 1.00), request.args.get("search"))
    energetic = "energetic"
    return render_template("mood.html", mood=energeticSongs, type=energetic)

# route when user mood is chill
@app.route("/chill")
def chill():
    chillSongs = get_mood_songs((0.20, 0.50), (0.40, 0.70), request.args.get("search"))
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
        
        elif request.form.get("delete"):
            songID = request.form.get("delete")
            session["favorites"].remove(songID)
            return redirect("/favorites")

        return "", 204

    if len(session["favorites"]) == 0:
        # condition allows to create the table in the favorites page
        songs = []

    else:
        # condition to display favorites in a table
        placeholders = ",".join(["?"] * len(session["favorites"]))
        query = f"""SELECT DISTINCT track_id, track_name, track_artist, 
                    track_popularity, track_album_name, track_album_release_date 
                    FROM songs WHERE track_id IN ({placeholders})"""
        songs = db.execute(query, session["favorites"]).fetchall()

    db.close()
    return render_template("favorites.html", songs=songs)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
