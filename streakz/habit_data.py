from flask import (
    Blueprint, render_template, redirect, request, url_for, jsonify, flash
)
from datetime import date, timedelta
from sqlalchemy import select, update, delete
from calendar import Calendar

from .models import db, Habit, Entry
from .forms import EditHabitForm


bp = Blueprint('habit_data', __name__)


@bp.route('/habit/<int:h_id>', methods=["GET"])
def habit_data(h_id):
    today = date.today()
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    cal = [d for d in Calendar().itermonthdates(today.year, today.month)]  # make a list dates by iterating over the generators returned by the itermonthdates function
    habit = db.session.scalar(select(Habit).where(Habit.id==h_id))
    entries = db.session.scalars(select(Entry).where(Entry.habit_id==h_id).where(Entry.date>=cal[0]).where(Entry.date<=cal[len(cal)-1]))
    entry_dates = [entry.date for entry in entries]
    form = EditHabitForm()
    return render_template("habit_data/habit_data.html", habit=habit, cal=cal, today=today, month=today.month, year=today.year, weekdays=weekdays, months=months, entry_dates=entry_dates, form=form)


@bp.route('/update_cal', methods=["POST"])
def update_cal():
    data = request.get_json()
    month = int(data["month"])
    year = int(data["year"])
    cal_dir = data["dir"]
    h_id = int(data["h_id"])
    response = {}

    if cal_dir == "prev":
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    elif cal_dir == "next":
        month += 1
        if month > 12:
            month = 1
            year += 1

    cal = [d for d in Calendar().itermonthdates(year, month)]  # make a list dates by iterating over the generators returned by the itermonthdates function
    habit = db.session.scalar(select(Habit).where(Habit.id==h_id))
    entries = db.session.scalars(select(Entry).where(Entry.habit_id==h_id).where(Entry.date>=cal[0]).where(Entry.date<=cal[len(cal)-1]))
    entry_dates = [entry.date for entry in entries]
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    calRawHTML = render_template('habit_data/cal.html', cal=cal, weekdays=weekdays, months=months, month=month, year=year, habit=habit, entry_dates=entry_dates)

    response = {
        "calRawHTML": calRawHTML,
        "new_month": month,
        "new_year": year,
        "cal_title": f"{months[month - 1]} {year}"
    }
    return jsonify(response)


@bp.route('/habit/<int:h_id>/update/<string:check_date>', methods=["POST"])
def update_habit_day(h_id, check_date):
    entry_date = date.fromisoformat(check_date)
    response = {}

    if entry_date > date.today():
        response = {
            "status": "fail",
            "date": check_date,
            "msg": "Can't add an entry for a future date",
        }
    else:
        entry = db.session.scalar(select(Entry).where(Entry.habit_id==h_id).where(Entry.date==check_date))
        if entry:
            db.session.delete(entry)
        else:
            new_entry = Entry(habit_id=h_id, date=entry_date)
            db.session.add(new_entry)

        curr_streak = count_current_streak(h_id)
        db.session.commit()

        response = {
            "status": "success",
            "habit_id": h_id,
            "curr_streak": curr_streak,
            "date": check_date,
            "msg": "entry deleted" if entry else "new entry added",
        }
    return jsonify(response)


@bp.route('/habit/<int:h_id>/delete', methods=["POST"])
def delete_habit(h_id):
    if request.method == "POST":
        db.session.execute(delete(Entry).where(Entry.habit_id == h_id))
        db.session.execute(delete(Habit).where(Habit.id == h_id))
        db.session.commit()
        flash("Habit successfully deleted!", "success")
        return redirect(url_for("index.index"))


@bp.route('/habit/<int:h_id>/edit', methods=["POST"])
def edit_habit(h_id):
    editHabitForm = EditHabitForm()
    if request.method == "POST" and editHabitForm.validate():
        title = editHabitForm.title.data
        desc = editHabitForm.desc.data
        if not title and not desc:
            flash("Enter a new title or new description (or both).", "info")
            return redirect(url_for("habit_data.habit_data", h_id=h_id))
        elif title and desc:
            db.session.execute(update(Habit).where(Habit.id == h_id).values(title=title, desc=desc))
        elif title:
            db.session.execute(update(Habit).where(Habit.id == h_id).values(title=title))
        elif desc:
            db.session.execute(update(Habit).where(Habit.id == h_id).values(desc=desc))
        db.session.commit()
        flash("Habit editing successful!", "success")
    else:
        errors = editHabitForm.title.errors
        for e in errors:
            flash(e, "danger")
    return redirect(url_for("habit_data.habit_data", h_id=h_id))


@bp.route('/habit/<int:h_id>/get-best-streak-url', methods=["GET"])
def get_best_streak(h_id):
    best_streak = count_best_streak(h_id)
    response = {
        "best_streak": best_streak,
        "status": "success",
    }
    return jsonify(response)


def count_current_streak(h_id:int):
    today = date.today()
    t_entry =  db.session.scalar(select(Entry).where(Entry.habit_id == h_id).where(Entry.date == today))
    y_entry =  db.session.scalar(select(Entry).where(Entry.habit_id == h_id).where(Entry.date == (today - timedelta(days=1))))
    if t_entry and not y_entry:
        return 1
    if not y_entry:
        return 0
    else:
        entry_list = db.session.scalars(select(Entry).where(Entry.habit_id==h_id).where(Entry.date<=today).order_by(Entry.date.desc())).all()
        filtered_entry_list = [entry_list[0]]
        for i in range(1, len(entry_list)):
            if entry_list[i].date == entry_list[i-1].date-timedelta(days=1):
                filtered_entry_list += [entry_list[i]]
            else:
                break
        return len(filtered_entry_list)


def count_best_streak(h_id:int):
    today = date.today()
    entry_list = db.session.scalars(select(Entry).where(Entry.habit_id == h_id).where(Entry.date <= today).order_by(Entry.date.desc())).all()
    if len(entry_list) != 0:
        streak = 1
        best_streak = 1
        last_date = entry_list[0].date
        for i in range(1, len(entry_list)):
            if entry_list[i].date == last_date - timedelta(days=1):
                streak += 1
            else:
                streak = 1
            if best_streak < streak:
                best_streak = streak
            last_date = entry_list[i].date
    else:
        best_streak = 0

    return best_streak


@bp.app_context_processor
def utility_processor():
    
    def current_streak(h_id):
        return count_current_streak(h_id)

    def best_streak(h_id):
        return count_best_streak(h_id)

    return dict(current_streak=current_streak, best_streak=best_streak)