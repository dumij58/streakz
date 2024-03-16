from flask import (
    Blueprint, render_template, redirect, request, url_for, jsonify
)
from datetime import date, timedelta
from sqlalchemy import select

from .models import db, Habit, Entry
from .forms import AddHabitForm
from .habit_data import count_current_streak


bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    today = date.today()
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    one_day = timedelta(days=1)
    cols = 7
    dates = [today-(one_day*i) for i in range(cols)]
    habits = db.session.scalars(select(Habit).order_by(Habit.id)).all()
    return render_template("index/index.html", dates=dates, weekdays=weekdays, habits=habits, cols=cols, today=today)


@bp.route('/add', methods=["GET", "POST"])
def add_habit():
    addHabitForm = AddHabitForm()

    if request.method == "POST" and addHabitForm.validate():
        new_habit = Habit(title=addHabitForm.title.data, desc=addHabitForm.desc.data)
        db.session.add(new_habit)
        db.session.commit()
        return redirect(url_for("index.index"))
    
    return render_template("index/add_habit.html", form=addHabitForm)


@bp.route('/fetch_habit_check/<int:h_id>/<string:check_date>', methods=["GET"])
def fetch_habit_check(h_id, check_date):
    entry = db.session.scalar(select(Entry).where(Entry.habit_id == h_id).where(Entry.date == check_date))
    check = True if entry else False

    response = {
        "check": check,
        "status": "success",
    }
    return jsonify(response)


@bp.route('/update_habit_check/<int:h_id>/<string:check_date>', methods=["POST"])
def update_habit_check(h_id, check_date):
    entry = db.session.scalar(select(Entry).where(Entry.habit_id == h_id).where(Entry.date == check_date))

    if entry:
        db.session.delete(entry)
    else:
        new_entry = Entry(habit_id = h_id, date = date.fromisoformat(check_date))
        db.session.add(new_entry)

    curr_streak = count_current_streak(h_id)
    db.session.commit()

    response = {
        "status": "success",
        "habit_id": h_id,
        "curr_streak": curr_streak,
        "msg": "entry deleted!" if entry else "new entry added!",
    }
    return jsonify(response)


@bp.route('/hello')
def hello():
    return "<h2>Hello, World!</h2>"