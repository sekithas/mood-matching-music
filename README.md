## Mood Matching Music

__Tech Stack:__

1. SQLite
2. Python
3. Flask
4. CSS
5. HTML
6. JavaScript
7. Bootstrap

## Description:
Mood Matching Music is a web application that recommends songs based on a user’s mood. Users can select from moods such as **happy, sad, energetic, or chill**, and the app displays a list of songs matching that mood. Users can also **add songs to their favorites** and clear their favorites list. The project uses a dataset from Kaggle (as a csv file), which was imported into a **SQLite database** (`songs.db`) to store song metadata such as track name, artist, popularity, album, and release date. The mood classification relies on valence and energy metrics, where valence represents musical positivity and energy represents intensity. Songs are selected based on ranges suitable for each mood, ensuring that the recommended tracks match the intended emotional tone. Randomizing the songs each time allows users to discover new music even if they select the same mood multiple times, making the experience more engaging. The mood tables show the song name, artist, popularity score (0-100) based on Spotify, on demand Spotify embedded preview of the song and an add to favorites button as the last column.

## Features:
- Select your mood from the home page and get 30 random songs in a table.
- Refresh the songs that were returned in the table using a button namely "New Song Set".
    - Useful if the songs returned in the current table is not of your taste. Gives the user a more dynamic app experience
- Songs are randomly selected, with popularity used as a ranking signal.
- Directly listen to a 30 second preview of the song from the app itself (Spotify preview embed).
    - Useful to determine if the songs are of your taste.
- In each mood, you can search for songs you want and add them to favorites.
- Add songs to your favorites list by clicking ⭐️.
    - Useful so you can view your songs later on.
    - Success box to know that you added the song successfully.
- View your favorite songs, and clear it by clicking on the danger button "Clear Favorites".
- Individually delete songs from favorites.
- Responsive table layout (using bootstrap) and animated text.
    - Provides a better UX.

### File Overview

- `app.py`: Main Flask application. Contains route handlers for the home page, mood-specific pages (happy, sad, energetic, chill), and the favorites page. Handles user sessions to store favorite songs. Queries the SQLite database for songs matching each mood and passes them to the templates.
- `songs.db`: SQLite database storing all song data, imported from a Kaggle CSV. Contains columns for track ID, name, artist, popularity, album name, album release date, valence, and energy.
- `templates/`: HTML templates for rendering pages:
    - `layout.html`: Base template that defines the HTML structure and loads CSS and Bootstrap.
    - `index.html`: Home page with mood selection buttons and link to favorites.
    - `mood.html`: Displays a table of songs matching a mood, with embedded Spotify previews and buttons to add favorites.
    - `favorites.html`: Displays the user’s favorite songs and allows clearing the list.
- `static/styles.css`: Custom CSS for styling the app, including background images, animated text, table layout, and responsive design.
- `static/js/favorites.js`: JavaScript code for adding songs to favorites without needing to reload page (AJAX) and having a timeout for the success message.
- `static/js/spotify_embed.js`: JavaScript code to display the preview in a separate container, only when the user wants, just below the preview button. Helped prevent 429, Too Many Requests.
- `static/js/mood.js`: JavaScript code to update live song table when the user types the artist/song name into search bar.

## Design Choices
- While databases were considered for favorites, sessions was chosen instead of databases because of its simplicity in implementation in a personal app.
- Specific valence and energy values were used for each route.
- Tables were used to display songs because it is clean and can be easily customized by bootstrap, compared to using lists that look unappealing. Specifically, responsive tables was chosen because of more visual appeal and more dynamic experience, horizontal scroll on mobile will allow embed to be properly shwon.
- Spotify embed is used instead of storing audio locally because it is simple and legal.

## Install dependencies
- pip install flask flask-session
