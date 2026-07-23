Hello. This is my first official project on GitHub. It's a habit tracker for logging daily habits and viewing your progress.

It started as a command-line tool, but now it also has a web interface built with Flask so you can use it in your browser.

## Before you can run it make sure:
- You have Python 3 installed
- You have `git` installed (to clone the repo)

## If you do, run the following in the terminal line by line. As in press enter after each line

### Option 1: Run the web version (recommended)

1. `git clone https://github.com/GlitchManiac1/Habit-Tracker2.git`
2. `cd Habit-Tracker2`
3. `python -m venv .venv` (creates a virtual environment so your Python packages don't clash with other projects)
4. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On Mac/Linux: `source .venv/bin/activate`
5. `pip install -r requirements.txt` (installs Flask and anything else needed)
6. `python app.py`
7. Open your browser and go to `http://127.0.0.1:5000`

### Option 2: Run the command-line version (the original)

1. `git clone https://github.com/GlitchManiac1/Habit-Tracker2.git`
2. `cd Habit-Tracker2`
3. `python tracker2.py`

The CLI still works exactly as it always did. The web version just gives you a nicer way to interact with the same database.
