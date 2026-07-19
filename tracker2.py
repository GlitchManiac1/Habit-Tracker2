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

cursor.execute(
    """CREATE TABLE IF NOT EXISTS user_list(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_habit TEXT NOT NULL UNIQUE
    );"""
)

#input a habit function
def log_habit():
    habit = input("Please enter a habit name: ").strip().lower()
    cursor.execute("SELECT user_habit FROM user_list")
    results = cursor.fetchall()
    results_list = [item[0] for item in results]
    if habit not in results_list:
        print("Habit inputted is not part of list. Please type the items in your list")
        for item in results_list:
            print(item)
        return
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
    cursor.execute("SELECT user_habit FROM user_list")
    activities = cursor.fetchall()
    for item in activities:
        if item[0] not in counts:
            counts[item[0]] = {"done":0 , "missed":0}
        
    for item in results:
        if item[0] not in counts:   
            counts[item[0]] = {"done": 0, "missed": 0}
        counts[item[0]][item[1]] += 1
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
        
def input_habit():
    print("Type out your habits, separating them with a comma")
    user_habit = input("Type here: ")
    user_list = [item.strip().lower() for item in user_habit.split(",")]
    for habit in user_list:
        try:
            cursor.execute("INSERT INTO user_list (user_habit) VALUES (?);",(habit,))
            connection.commit()
        except sqlite3.IntegrityError:
            print(f"Habit '{habit}' already exists in the list")
    return user_list
        

def delete_habit():
    cursor.execute("SELECT DISTINCT user_habit FROM user_list")
    results = cursor.fetchall()
    habit_list = [item[0] for item in results]
    for item in habit_list:
        print(item)
    while True:
        habit = input("Which habit do you want to delete? If you want to delete all type 'all' ").lower()
        if habit == "all":
            cursor.execute("DELETE FROM user_list")
            connection.commit()
            break

        elif habit in habit_list:
            cursor.execute("DELETE FROM user_list WHERE user_habit = ?",(habit,))
            connection.commit()
            break

        else:
           print("Habit is not in list. Please try again")
    
    cursor.execute("SELECT DISTINCT user_habit FROM user_list")
    results = cursor.fetchall()
    habit_list = [item[0] for item in results]
    for item in habit_list:
        print(item)



def main():
    print("If this is your first time please input a list of habits you would like keep track of.")
    print("When you complete a habit, log the habit.")
    print("please note that for efficient use, the habits should be in the same tense")
    print("Eg: If 'read' is inputted, do not log 'reading' as the habit, just 'read'")
    while True:
        print("\n--- Habit Tracker ---")
        print("1.Input the habits you would like to track")
        print("2. Log a habit")
        print("3. View progress")
        print("4. Get streak for specific habit")
        print("5. Delete Habit")
        print("6. Quit")
        choice = input("Choose an option: ").strip()

        if choice =="1":
            input_habit()
        elif choice == "2":
            log_habit()
        elif choice == "3":
            result = view_progress()
            for habit_name, status_counts in result.items():
                streak = get_streak(habit_name)
                print(f"{habit_name}: {status_counts['done']} done, {status_counts['missed']} missed, streak: {streak}")
        
        elif choice == "4":
            habit = input("Type a valid habit: ")
            print(get_streak(habit))
        
        elif choice == "5":
            break     
            
        elif choice == "6":
            delete_habit()
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()