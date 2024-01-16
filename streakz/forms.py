from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError

class AddHabitForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Habit title is required.")])
    desc = StringField('Description', validators=[Optional()])
    submit = SubmitField('Add')