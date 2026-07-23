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

if __name__ == "__main__":
    app.run(debug=True)