# Streakz : Habit Tracker

#### Video Demo: https://youtu.be/6A8PR5u6LLg

#### Description:
Streakz is a simple and straightforward web-based tool that keeps track of your daily habits. By leveraging the power of streaks, it encourages you to stay committed to completing your habits every day.

<br>

<details>

<summary>Want to test Streakz ?</summary>
<br>

```shell
# Make a new directory (Choose any name for the directory) and go inside it
mkdir test
cd test

# Create python virtual environment
python3 -m venv venv

# Activate venv
## Linux
source venv/bin/activate
## Windows (CMD)
venv\Scripts\activate.bat
## Windows (PowerShell)
venv\Scripts\Activate.ps1

# Clone Streakz repository
git clone https://github.com/dumij58/streakz.git

# cd into streakz directory
cd streakz

# install requirements
pip install -r requirements.txt

# Run flask development server
flask --app project.py run
# if you get an error try another port using
flask --app project.py run -p $PORT_NUMBER
```

#### When you are done testing
```shell
deactivate
```

<br>

</details>


<details>

<summary>See what each Python file does</summary>

### project.py

This file sets up the flask application, sets the default config values, loads the configuration file if it exists and overwrites the existing config values, creates the instance folder if it doesn't exist, initializes SQLAlchemy and creates all the tables in the database using the models set up in models.py if there is no tables in the database, sets up flask routes and functions.

### models.py

This file sets up SQLAlchemy. It contains all the models for all tables in the database and it sets up the relationships between the models.

### forms.py

This file contains all the WTForms's forms used in the project and custom validators to validate the form data.

### test_project.py

Contains all the tests for flask routes and functions in project.py. Use pytest to test the application.

</details>


<br>

## Index Page

Index Page is the homepage of Streakz.

It consists of a navbar with the icon and the name "Streakz", "Add Habit" button, all the habits in the database with the status of each habit in the last 7 days and the current streak of each habit.

You can,
- See the habit title and part of the habit's decsription
- See the current streak of each habit
- Check/Uncheck a habit within the last 7 days
- See the current streak update accordingly when a check/uncheck occur

<br>

Clicking on "Add Habit" button will take you to the "Add Habit Page"

If you want to check/uncheck habits beyond the last 7 days or if you want to edit a habit you can simply click on a habit and it will take you to the "Habit Page".


## Add Habit Page

In here you can specify a title for the new habit and a description, and then click "Add" to add it to the database.

Title is required, but the desciption is optional.

Data is being validated using flask-wtf and wtforms.

## Habit Page

In here you will see every detail about the habit you have selected.

In the habit details section you will see the habit title, habit description, an edit button (which will let you edit the habit title and/or habit description) and a delete button to delete the habit entirely.

In the "Streaks" section you will see the current streak and the best streak of the habit.

In the "Calender" section you will get a full-fledged calender that indicates all the checked days of the selected habit. You can cycle through the months to see the history of your habit. And also check/uncheck any day on the calender. (Can only check/uncheck upto present day, can't check/uncheck future dates.) Updating any day will also update the current streak and best streak accordingly.
