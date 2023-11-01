import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import requests


from helpers import apology, login_required

# Configure application
app = Flask(__name__)

def search_movie(movie_name):
    api_key = '925bbfd8574af2988916115dd5add180'
    base_url = 'https://api.themoviedb.org/3'

    search_url = f'{base_url}/search/movie'

    params = {
        'api_key': api_key,
        'query': movie_name
    }

    response = requests.get(search_url, params=params)
    first_movie = None
    if response.status_code == 200:
        search_results = response.json()
        if search_results['results']:
            for movie in search_results['results']:
                if movie_name.lower() == movie['title'].lower():
                    first_movie = movie
                    break

            if not first_movie:
                return None
            if first_movie:
                movie_id = first_movie['id']
                movie_details_url = f'{base_url}/movie/{movie_id}'

                details_params = {
                    'api_key': api_key
                }
                details_response = requests.get(movie_details_url, params=details_params)

                if details_response.status_code == 200:
                    movie_details = details_response.json()
                    genres = movie_details['genres']
                    first_movie['genres'] = [genre['name'] for genre in genres]

                    return first_movie
                else:
                    print(f'Não foi possível obter detalhes para o filme "{movie_name}"')
                    return None
    return None


def get_movie_images(movie_id):
    api_key = '925bbfd8574af2988916115dd5add180'
    base_url = 'https://api.themoviedb.org/3'

    movie_images_url = f'{base_url}/movie/{movie_id}/images'

    params = {
        'api_key': api_key
    }

    response = requests.get(movie_images_url, params=params)

    if response.status_code == 200:
        images_data = response.json()
        posters = images_data['posters']
        return [f"https://image.tmdb.org/t/p/original{poster['file_path']}" for poster in posters]
    else:
        return None



genres = [
    {"name":"Action", "id":28},
    {"name":"Adventure", "id":12},
    {"name":"Comedy", "id":35},
    {"name":"Animation", "id":16},
    {"name":"Crime", "id":80},
    {"name":"Documentary", "id":99},
    {"name":"Drama", "id":18},
    {"name":"Family", "id":10751},
    {"name":"Fantasy", "id":14},
    {"name":"Science Fiction", "id":878},
    {"name":"Horror", "id":27},
    {"name":"Mistery", "id":9648},
    {"name":"Romance", "id":10749},
    {"name":"Thriller", "id":53},
    {"name":"War", "id":10752},
    {"name":"Musical", "id":10402},
    {"name":"Western", "id":37}
]

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    favorite_movies = db.execute("SELECT movie_name, movie_overview, image_url, rating, genres FROM favorite_movie WHERE user_id = ?",user_id)
    return render_template("index.html", favorite_movies=favorite_movies)


@app.route("/genre")
@login_required
def genre():
    """Show history of transactions"""
    genres_list = db.execute("SELECT genre_name FROM preference_genre ORDER BY genre_count DESC")
    return render_template("genre.html", genres=genres_list)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Must provide username" )

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="Must provide password" )

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="Invalid username and/or password" )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/List", methods=["GET", "POST"])
@login_required
def List():
    """Get stock quote."""
    if request.method == "POST":
        movie_name = request.form.get("movie_name")

        if not movie_name:
            return render_template("error.html", message="Must give one movie name!")


        if search_movie(movie_name):
            movie = search_movie(movie_name)
        else:
            return render_template("error.html", message="There is no movie named {name}".format(name=movie_name))

        user_id = session["user_id"]
        title = movie["title"]
        overview = movie["overview"]
        movie_id = movie["id"]
        if get_movie_images(movie_id):
            images = get_movie_images(movie_id)
        else:
            return render_template("error.html", message="There is no movie named {name}".format(name=movie_name))
        genres = None
        genres_db = movie["genres"]
        for genre in genres_db:
            if genre == genres_db[0]:
                genres = genre
            else:
                genres += "{name} ".format(name=genre)


        db.execute("INSERT INTO search_movie (movie_name, user_id) VALUES (?, ?)", movie_name, user_id)


        return render_template("listed.html", title=title, overview=overview, image=images[0], name=movie_name, genre=genres)
    else:
        return render_template("list.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":

        return render_template("register.html", genres=genres)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        genre = request.form.get("genres")

        if not username:
            return render_template("error.html", message="Must insert a username!")
        elif not genre:
            return render_template("error.html", message="You must select your favorite genre!")
        elif not password:
            return render_template("error.html", message="Must insert a password!")
        elif not confirmation:
            return render_template("error.html", message="Must confirm the password!")
        elif password != confirmation:
            return render_template("error.html", message="The passwords are not equal!")


        user = db.execute("SELECT username FROM users WHERE username = ?", username)

        if len(user) != 0:
            return render_template("error.html", message="This username has already been taken")

        new_user = db.execute("INSERT INTO users (username, hash, favorite_genre) VALUES (?, ?, ?)", username, generate_password_hash(password), genre)

        session["user_id"] = new_user


        return redirect("/")




@app.route("/Listed", methods=["GET", "POST"])
@login_required
def Listed():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("listed.html")
    else:
        if not request.form.get("movie_rating"):
            return render_template("error.html",message="Must tell the rating to add to the list!")
        elif not(int(request.form.get("movie_rating")) >= 0 and int(request.form.get("movie_rating")) <= 10):
            return render_template("error.html",message="The rating number must be between 0 and 10!")

        user_id = session["user_id"]
        result = db.execute("SELECT movie_name FROM search_movie WHERE user_id = ? ORDER BY id DESC LIMIT 1", user_id)
        movie_name = result[0].get('movie_name', '')
        if search_movie(movie_name):
            movie = search_movie(movie_name)
        else:
            return render_template("error.html", message="There is no movie named {name}".format(name=movie_name))
        movie = search_movie(movie_name)
        movie_id = movie["id"]
        rating = request.form.get("movie_rating")
        genres = None
        genres_db = movie["genres"]
        for genre in genres_db:
            if genre == genres_db[0]:
                genres = "{name}".format(name=genre)
            else:
                genres += ", {name}".format(name=genre)
        for genre in genres_db:
            if len(db.execute("SELECT genre_name FROM preference_genre WHERE user_id = ? and genre_name = ?",user_id,genre)) == 0:
                db.execute("INSERT INTO preference_genre (genre_name, genre_count, user_id) VALUES (?, ?, ?)", genre, 1, user_id)
            else:
                genre_count = db.execute("SELECT genre_count FROM preference_genre WHERE user_id = ? and genre_name  = ?", user_id, genre)
                count = genre_count[0].get("genre_count",'')
                db.execute("UPDATE preference_genre SET genre_count = ? WHERE user_id = ? and genre_name = ?", count + 1, user_id, genre)

        if get_movie_images(movie_id):
            images = get_movie_images(movie_id)
        else:
            return render_template("error.html", message="There is no movie named {name}".format(name=movie_name))
        overview = movie["overview"]
        if len(db.execute("SELECT movie_name FROM favorite_movie WHERE user_id = ? and movie_name = ?", user_id, movie_name)) != 0:
            return render_template("error.html", message="You are already have {name} in your list!".format(name=movie_name))

        db.execute("INSERT INTO favorite_movie (movie_id, movie_name, rating, user_id, movie_overview, image_url, genres) VALUES (?, ?, ?, ?, ?, ?, ?)",movie_id, movie_name, rating, user_id, overview, images[0], genres)

        flash("{name} was added to your movie list!".format(name=movie_name))

        return redirect("/")

