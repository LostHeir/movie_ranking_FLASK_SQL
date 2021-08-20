from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from model import EditForm
import requests

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

new_movie = Movie(
    title="Phone Boothsda",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
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


if __name__ == '__main__':
    app.run(debug=True)
