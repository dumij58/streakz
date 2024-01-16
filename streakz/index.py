from flask import (
    Blueprint, render_template, redirect, request, url_for
)
from datetime import date
from sqlalchemy import select

from .models import db, Habit, Entry
from .forms import AddHabitForm


bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    d = date.today().day
    days = [f"{day:0>2d}" for day in range(d, d-7, -1)]
    habits = db.session.scalars(select(Habit).order_by(Habit.id)).all()
    return render_template("index/index.html", days=days, habits=habits)

@bp.route('/add', methods=["GET", "POST"])
def add_habit():
    addHabitForm = AddHabitForm()

    if request.method == "POST" and addHabitForm.validate():
        new_habit = Habit(title=addHabitForm.title.data, desc=addHabitForm.desc.data)
        db.session.add(new_habit)
        db.session.commit()
        return redirect(url_for("index.index"))
    
    return render_template("index/add_habit.html", form=addHabitForm)