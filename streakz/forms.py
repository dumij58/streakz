from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from sqlalchemy import select

from streakz.models import db, Habit


def check_habit(form, field):
    title = str(field.data).strip()
    if db.session.scalar(select(Habit).where(Habit.title == title)):
        raise ValidationError(message="Habit with the same title already exist.")


class AddHabitForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Habit title is required."),
        check_habit,
        ])
    desc = StringField('Description', validators=[Optional()])
    submit = SubmitField('Add')