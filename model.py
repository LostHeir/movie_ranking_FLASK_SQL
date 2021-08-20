from wtforms import SubmitField, FloatField, StringField, PasswordField, validators
from flask_wtf import Form


class EditForm(Form):
    rating = FloatField("Your rating:")
    review = StringField("Your review:")
    submit = SubmitField("Done")

