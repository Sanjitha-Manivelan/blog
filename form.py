from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = IntegerField("ID of Drinks: ")
    submit = SubmitField("Add Drink")

    def __repr__(self):
        return name

class DelForm(FlaskForm):
    id = IntegerField("Id Number of Drink to Remove:")
    submit = SubmitField("Remove Drink")