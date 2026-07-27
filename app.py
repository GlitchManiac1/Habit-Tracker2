from flask import Flask,render_template,request
import tracker2
app = Flask(__name__)

@app.route("/")
def home():
    result = tracker2.view_progress()
    habit = []
    
    for habit_name, status_counts in result.items():
        streak = tracker2.get_streak(habit_name)

        habit.append({
            'name':habit_name,
            'done':status_counts['done'],
            'missed':status_counts['missed'],
            'streak':streak
        })
        
    return render_template('template.html',habits=habit)

@app.route("/log", methods=["GET","POST"])
def log():
    if request.method == "POST":
        habit = request.form.get("habit")
        status = request.form.get("status")
        success = tracker2.log_habit(habit,status)
        if success:
            return render_template(
                'message.html',
                success=True,
                message="Your habit has been logged successfully!",
                redirect_url="/"
            )
        else:
            return render_template(
                'message.html',
                success=False,
                message="Failed to log habit. It may already be logged today or doesn't exist.",
                redirect_url="/log"
            )
        
    habit_list = tracker2.habit_list()
    return render_template('log.html', habits=habit_list)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        habits_text = request.form.get("habits")
        if habits_text:
            habit_list = [habit.strip().lower() for habit in habits_text.split(",") if habit.strip()]
            tracker2.input_habit(habits_text)

            return render_template(
                'message.html',
                success=True,
                message=f"Added {len(habit_list)} habit(s) successfully!",
                redirect_url="/"
            )

        else:
            return render_template(
                'message.html',
                success=False,
                message="No habits entered. Please try again.",
                redirect_url="/add"
            )

    return render_template('add.html')

@app.route("/delete", methods=["GET","POST"])
def delete():
    if request.method == "POST":
        habit = request.form.get("habit")
        success = tracker2.delete_habit(habit)
        if success:
            return render_template(
                'message.html',
                success=True,
                message="Your habit has been deleted successfully!",
                redirect_url="/"
            )
        else:
            return render_template(
                'message.html',
                success=False,
                message="Failed to delete habit. It doesn't exist.",
                redirect_url="/delete"
            )
    habit_list = tracker2.habit_list()
    return render_template('delete.html', habits=habit_list)
    
        
        
if __name__ == "__main__":
    app.run(debug=True)