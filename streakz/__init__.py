import os

from flask import Flask

from .models import db, migrate

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= "dev",

        # configure the SQLite database, relative to the app instance folder
        SQLALCHEMY_DATABASE_URI = "sqlite:///streakz.db",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize the app with flask-sqlalchemy and flask-migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # create models defined in models.py
    with app.app_context():
        db.create_all()

    # import and register blueprints
    from . import index, habit_data
    app.register_blueprint(index.bp)
    app.register_blueprint(habit_data.bp)

    return app