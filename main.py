from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from model import EditForm, AddForm
import requests

API_KEY = "b055eef3436622ce621ea5fb6387d4e1"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Create data base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-toplist.db'
# Silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)


# Create table in the data base
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Movie: {self.title}"


# Create data base
# db.create_all()


@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating.asc()).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route("/update", methods=["GET", "POST"])
def update():
    movie_id = request.args.get("id")
    selected_movie = Movie.query.get(movie_id)
    form = EditForm(request.form)
    if request.method == "GET":
        form.rating.data = selected_movie.rating  # set default value
        form.review.data = selected_movie.review  # set default value
    if form.validate_on_submit():
        selected_movie.rating = form.rating.data
        selected_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=selected_movie, form=form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm(request.form)
    if form.validate_on_submit():
        params = dict(api_key=API_KEY, query=form.title.data)
        response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=params).json()
        return render_template("select.html", movies=response["results"])
    return render_template("add.html", form=form)


@app.route("/select")
def select():
    movie_id = request.args.get("id")
    params = dict(api_key=API_KEY)
    response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=params).json()
    new_movie = Movie(
        title=response["original_title"],
        year=response["release_date"].split("-")[0],  # date in format yyyy-mm-dd, get only the year
        description=response["overview"],
        rating=0,
        ranking=0,
        review="",
        img_url="https://image.tmdb.org/t/p/w500"+response["poster_path"]  # add last part of the poster url from API
    )
    db.session.add(new_movie)
    db.session.commit()

    movies = Movie.query.all()  # get all movies and find the last one, to pass id for edit form
    added_movie_id = movies[-1].id

    return redirect(url_for("update", id=added_movie_id))

if __name__ == '__main__':
    app.run(debug=True)
