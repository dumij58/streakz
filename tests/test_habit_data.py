import pytest
import re

from datetime import date, timedelta
from streakz.habit_data import count_current_streak
from conftest import get_habits, get_entries

@pytest.mark.parametrize(('test_habit_no', 'title', 'desc', 'entry_day'), (
    (1, b'Test Habit 1', b'This is a test habit w/ a description', f"{(date.today()-timedelta(days=5)).day:>02d}"),
    (2, b'Test Habit 2', b'', f"{date.today().day:>02d}"),
))
def test_habit_data(client, habits, test_habit_no, title, desc, entry_day):
    response = client.get(f"/habit/{habits[test_habit_no-1].id}")
    assert response.status_code == 200
    assert title in response.data
    assert desc in response.data
    assert re.search(rf"btn-(?:outline-)?primary.*{entry_day}", response.text)


@pytest.mark.parametrize(('test_habit_no', 'year', 'month', 'dir', 'new_year', 'new_month', 'entry_day'), (
    (1, "2023", "1", "prev", 2022, 12, "23"),       # 2022-12-23
    (1, "2019", "12", "next", 2020, 1, "30"),       # 2020-01-30
    (2, "2018", "5", "prev", 2018, 4, "27"),        # 2018-04-27
    (2, "2020", "4", "next", 2020, 5, "8"),         # 2020-05-08
))
def test_update_cal(client, habits, test_habit_no, year, month, dir, new_year, new_month, entry_day):
    data = {
            "month": month,
            "year": year,
            "dir": dir,
            "h_id": habits[test_habit_no-1].id,
       }
    response = client.post(f"/update_cal", json=data)
    assert response.status_code == 200
    assert response.json["new_year"] == new_year
    assert response.json["new_month"] == new_month
    assert re.search(rf"btn-primary.*{entry_day}", response.json["calRawHTML"])


@pytest.mark.parametrize(('test_habit_no', 'check_date', 'msg'), (
    (1, date.today()-timedelta(days=1), "entry deleted"),
    (1, date.today()-timedelta(days=5), "entry deleted"),
    (2, date.today(), "entry deleted"),
    (2, date.today()-timedelta(days=32), "entry deleted"),

    (1, date.today(), "new entry added"),
    (2, date.today()-timedelta(days=5), "new entry added"),

    (2, date.today()+timedelta(days=1), "Can't add an entry for a future date"),
))
def test_update_habit_day(client, habits, test_habit_no, check_date, msg):
    response = client.post(f"/habit/{habits[test_habit_no-1].id}/update/{check_date}")
    assert response.status_code == 200
    assert response.json["msg"] == msg


@pytest.mark.parametrize(('test_habit_no'), (
    (1),
    (2),
))
def test_delete_habit(client, habits, test_habit_no):
    response = client.post(f"/habit/{habits[test_habit_no-1].id}/delete")
    assert response.status_code == 302
    assert get_entries([habits[test_habit_no-1].id]) == []
    assert get_habits(h_ids=[habits[test_habit_no-1].id]) == []


@pytest.mark.parametrize(('test_habit_no', 'title', 'desc', 'msg'), (
    (1, 'Test Habit 1 w/ description', '', b'Test Habit 1 w/ description'),
    (2, '', 'This is a test habit with a description', b'This is a test habit with a description'),
    (1, '', '', b'Enter a new title or new description (or both).'),
    (2, 'Test Habit 1', '', b'Habit with the same title already exist.'),
))
def test_edit_habit(client, habits, test_habit_no, title, desc, msg):
    response = client.post(f"/habit/{habits[test_habit_no-1].id}/edit", data={"title": title, "desc": desc}, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == f"/habit/{habits[test_habit_no-1].id}"
    assert msg in response.data


@pytest.mark.parametrize(('test_habit_no', 'curr_streak'), (
    (1, 1),
    (2, 1),
    (3, 4),
))
def test_count_current_streak(client, habits, test_habit_no, curr_streak):
    assert count_current_streak(habits[test_habit_no-1].id) == curr_streak


@pytest.mark.parametrize(('test_habit_no', 'best_streak'), (
    (1, 1),
    (2, 1),
    (3, 13),
))
def test_get_best_streak(client, habits, test_habit_no, best_streak):
    response = client.get(f"/habit/{habits[test_habit_no-1].id}/get-best-streak-url")
    assert response.status_code == 200
    assert response.json["best_streak"] == best_streak