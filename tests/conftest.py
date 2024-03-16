import os
import pytest
from sqlalchemy import insert, select
from datetime import date, timedelta

from streakz.models import Habit, Entry
from streakz.models import db, Habit, Entry


@pytest.fixture
def app():
    from streakz import create_app

    test_config = {
        "TESTING": True,
        "SECRET_KEY": "test",
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
    }

    app = create_app(test_config=test_config)

    with app.app_context():

        habits = db.session.scalars(
            insert(Habit).returning(Habit),
            [
                {"title": "Test Habit 1", "desc": "This is a test habit w/ a description"},
                {"title": "Test Habit 2", "desc": ""},
                {"title": "Test Habit 3", "desc": "This is to test streak tracking"},
            ]
        ).all()
        db.session.execute(
            insert(Entry),
            [
                {"habit_id": habits[0].id, "date": date.today()-timedelta(days=1)},
                {"habit_id": habits[0].id, "date": date.today()-timedelta(days=5)},
                {"habit_id": habits[0].id, "date": date.fromisoformat("2022-12-23")},
                {"habit_id": habits[0].id, "date": date.fromisoformat("2020-01-30")},

                {"habit_id": habits[1].id, "date": date.today()},
                {"habit_id": habits[1].id, "date": date.today()-timedelta(days=32)},
                {"habit_id": habits[1].id, "date": date.fromisoformat("2018-04-27")},
                {"habit_id": habits[1].id, "date": date.fromisoformat("2020-05-08")},

                {"habit_id": habits[2].id, "date": date.today()-timedelta(days=1)},
                {"habit_id": habits[2].id, "date": date.today()-timedelta(days=2)},
                {"habit_id": habits[2].id, "date": date.today()-timedelta(days=3)},
                {"habit_id": habits[2].id, "date": date.today()-timedelta(days=4)},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-08")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-09")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-10")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-11")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-12")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-13")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-14")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-15")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-16")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-17")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-18")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-19")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-20")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-26")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-27")},
                {"habit_id": habits[2].id, "date": date.fromisoformat("2023-05-28")},
            ]
        )

        yield app

        os.remove("instance/test.db")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def habits():
    return get_habits(h_titles=["Test Habit 1", "Test Habit 2", "Test Habit 3"])


def get_habits(**kwargs):
    if "h_ids" in kwargs:
        return db.session.scalars(select(Habit).where(Habit.id.in_(kwargs["h_ids"]))).all()
    elif "h_titles" in kwargs:
        return db.session.scalars(select(Habit).where(Habit.title.in_(kwargs["h_titles"]))).all()


def get_entries(h_ids):
    return db.session.scalars(select(Entry).where(Entry.habit_id.in_(h_ids))).all()
