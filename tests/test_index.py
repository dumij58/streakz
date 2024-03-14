import pytest

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/add">Add Habit</a>' in response.data
    assert b'Test Habit 1' in response.data
    assert b'This is a test habit w/ a description' in response.data
    assert b'Test Habit 2' in response.data


@pytest.mark.parametrize(('title', 'desc'), (
    ('New Habit 1', 'This is a new habit'),
))
def test_add_habit(client, title, desc):
    get = client.get("/add")
    assert get.status_code == 200
    assert b'method="POST"' in get.data
    assert b'Title' in get.data
    assert b'Description' in get.data
    assert b'type="submit"' in get.data

    post = client.post("/add", data={"title": title, "desc": desc}, follow_redirects=True)
    assert post.status_code == 200
    assert len(post.history) == 1
    assert post.request.path == "/"


@pytest.mark.parametrize(('title', 'desc', 'message'), (
    ('', 'description', b'Habit title is required.'),
    ('Test Habit 1', '', b'Habit with the same title already exist.'),
))
def test_add_habit_validate(client, title, desc, message):
    response = client.post("/add", data={"title": title, "desc": desc})
    assert response.status_code == 200
    assert len(response.history) == 0
    assert response.request.path != "/"
    assert message in response.data