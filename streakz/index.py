from flask import (
    Blueprint, render_template, redirect, request, url_for, jsonify
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
    return render_template("index/index.html", days=days, habits=habits, datelib=date)


@bp.route('/add', methods=["GET", "POST"])
def add_habit():
    addHabitForm = AddHabitForm()

    if request.method == "POST" and addHabitForm.validate():
        new_habit = Habit(title=addHabitForm.title.data, desc=addHabitForm.desc.data)
        db.session.add(new_habit)
        db.session.commit()
        return redirect(url_for("index.index"))
    
    return render_template("index/add_habit.html", form=addHabitForm)


@bp.route('/fetch_habit_check/<int:h_id>/<day>', methods=["GET"])
def fetch_habit_check(h_id, day):
    check_date = date.today().replace(day=int(day))
    entry = db.session.scalar(select(Entry).where(Entry.habit_id==h_id).where(Entry.date==check_date))
    check = True if entry else False

    response = {
        "check": check,
        "status": "success",
    }

    return jsonify(response)


@bp.route('/update_habit_check/<int:h_id>/<check_date>', methods=["POST"])
def update_habit_check(h_id, check_date):
    entry = db.session.scalar(select(Entry).where(Entry.habit_id==h_id).where(Entry.date==check_date))
    print(entry)

    if entry:
        db.session.delete(entry)
        print(db.session.commit())
        
    else:
        new_entry = Entry(habit_id=h_id, date=date.fromisoformat(check_date))
        db.session.add(new_entry)
        print(db.session.commit())

    response = {
        "status": "success",
        "msg": "entry deleted!" if entry else "new entry added!",
    }
    return jsonify(response)