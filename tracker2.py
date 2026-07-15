import datetime
import sqlite3

#creation of database file habits.db
connection = sqlite3.connect("habits.db")
cursor = connection.cursor()

#creation of habits table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS habits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_logged TEXT NOT NULL,
            habit_name TEXT NOT NULL,
            status TEXT NOT NULL
    );"""
)

#input a habit function
def log_habit():
    habit = input("Please enter a habit name: ")

    answer = already_logged_today(habit)
    if answer == True:
        print("You already logged that habit today")
        return
    
    affirm = input("Was it done or missed: ").strip().lower()

    date = str(datetime.date.today())

    record = (date,habit,affirm)
    cursor.execute("INSERT INTO habits (date_logged,habit_name,status) VALUES (?,?,?);",record)
    connection.commit()


def view_progress():
    counts = {}
    cursor.execute("SELECT habit_name,status FROM habits")
    results = cursor.fetchall()
    for item in results:
    
        if item[0] not in counts:
            counts[item[0]] = {"done":0 , "missed":0}
        counts[item[0]][item[1]] +=1
    return counts


def already_logged_today(habit_name):
    state = False
    date_today = str(datetime.date.today())
    cursor.execute("SELECT date_logged,habit_name FROM habits WHERE date_logged=? AND habit_name=?", (date_today,habit_name))
    results = cursor.fetchall()
    if len(results) != 0:
        state = True
    return state
   
def get_streak(habit_name):
    cursor.execute("SELECT date_logged FROM habits WHERE habit_name =? AND status=? ORDER BY date_logged DESC", (habit_name,"done"))
    results = cursor.fetchall()
    streak = 0
    for item in results:
        if item[0]==str(datetime.date.today()-datetime.timedelta(days=streak)):
            streak+=1
        else:
            break
    return streak   
        

def main():
    while True:
        print("\n--- Habit Tracker ---")
        print("1. Log a habit")
        print("2. View progress")
        print("3. Get streak for specific habit")
        print("4. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            log_habit()
        elif choice == "2":
            result = view_progress()
            for habit_name, status_counts in result.items():
                streak = get_streak(habit_name)
                print(f"{habit_name}: {status_counts['done']} done, {status_counts['missed']} missed, streak: {streak}")
        
        elif choice == "3":
            habit = input("Type a valid habit: ")
            print(get_streak(habit))
        
        elif choice == "4":
            break     
            
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()