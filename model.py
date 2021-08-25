from wtforms import SubmitField, FloatField, StringField
from wtforms.validators import DataRequired
from flask_wtf import Form


class EditForm(Form):
    rating = FloatField("Your rating:")
    review = StringField("Your review:")
    submit = SubmitField("Done")


class AddForm(Form):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")
