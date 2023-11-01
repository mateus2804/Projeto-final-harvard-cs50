# YOUR PROJECT TITLE: YOUR Movies
#### Video Demo:  <https://youtu.be/zzzE030PVU0>
#### Description:
# Motivation to the project:
Currently, while I was taking the CS50 course, I was also taking an actual CS course on UVV, Brazil, so, because of that, I was searching for a internship and many of the offers I had received asked for python experience e and SQL (CRUD), so, for this purpose, I joined my interests in movies and my need to learn python and had the idea to create an app in python/flask, sql and html/css to search and list for the user's favorites movies.
# How it was made:
To the construction of this app, I used TMDB API(https://www.themoviedb.org/?language=pt-BR), Python, SQLite, HTML and CSS. It is not my purpose to increase my ability with CSS, so I used the layout of problem set 9, I also used some of the helpers.py functions. The files I have made are these listed:
## Files:
### app.py (Project/app.py)
In this file, there are two API fetch functions (search_move, search_movie_image) and 7 routes to 7 seven html files
### project.db (Project/project.db)
This is the database I used on this app, it has tables to store user data, genre data and the data of the movies in the list:
.schema:
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, favorite_genre INTEGER);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE search_movie  (movie_name TEXT, user_id INTEGER NOT NULL, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL);
CREATE TABLE favorite_movie  (movie_id INTEGER, movie_name TEXT, rating INTEGER, user_id INTEGER NOT NULL, movie_overview TEXT, image_url TEXT, genres TEXT);
CREATE TABLE preference_genre (genre_name TEXT, genre_count INTEGER, user_id INTEGER);
### styles.css (Project/static/styles.css)
This is the css file that was already made in pset 9 and use some bootstraps to personalize the html:
#### <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" rel="stylesheet">
#### <script crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"></script>
### x.html ((Project/templates/.) - layout.html)
These are all the html files I used create my pages in the app:
error.html: layout for error advise
index.html: main page
listed/list.html: search and add to list page
genre.html: page for see the recommended genres
### layout.html (Project/templates/layout.html)
That html file is the base design for all the others html pages
# Conclusion
In conclusion, I think my final project fits perfectly in the proposed criteria. The only thing that I think I could maybe improve is the way the app was made, my first plans were to construct the app entirely in react native / javascript, but I had many problems with javaScript due to lack of experience.

