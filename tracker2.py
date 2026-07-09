import datetime

FILENAME = "habits.txt"

def already_logged_today(habit_name):
    # TODO:
    state = False
    date_today = str(datetime.date.today())
    # 1. Get today's date as a string (same way you did in log_habit)
    with open(FILENAME, "r") as f:
        for line in f:
            splitup = line.strip().split(",")
            if splitup[0] == date_today:
                if splitup[1] == habit_name:
                    state = True
                    break
                else:
                    continue
            else:
                continue
    return state
    # 2. Open FILENAME in read mode
    # 3. Loop through each line, split it like you did in view_progress
    # 4. If a line's date matches today AND habit_name matches,
    #    return True
    # 5. If you finish the loop without finding a match, return False
    pass

def log_habit():
    # TODO:
    # 1. Ask the user (input()) for a habit name
    habit = input("Please enter a habit name: ")

    answer = already_logged_today(habit)
    if answer == True:
        print("You already logged that habit today")
        return

    # 2. Ask the user whether it was "done" or "missed"
    affirm = input("Was it done or missed: ").strip().lower()
    # 3. Get today's date (hint: datetime.date.today())
    date = str(datetime.date.today())
    # 4. Open FILENAME in "append" mode and write a line like:
    #    2026-07-09,workout,done
    with open(FILENAME,"a") as f:
        f.write(date + "," + habit + "," + affirm + "\n")

    pass

def view_progress():
    # TODO:
    # 1. Open FILENAME in "read" mode ("r")
    counts = {}
    with open(FILENAME,"r") as f:
        for line in f:
            parts = line.strip().split(",")
            date = parts[0]
            habit_name = parts[1]
            status = parts[2]
            if habit_name not in counts:
                counts[habit_name] = {"done":0, "missed":0} 
            counts[habit_name][status]+= 1
    return counts

    # 2. Loop over each line in the file
    # 3. For each line, split it by "," into date, habit_name, status
    #    (hint: line.strip().split(","))
    # 4. Keep count of "done" and "missed" per habit
    #    (hint: use a dictionary, e.g. counts = {})
    # 5. After the loop, print a summary like:
    #       workout: 3 done, 1 missed
    #       read: 2 done, 0 missed
    pass

def main():
    while True:
        print("\n--- Habit Tracker ---")
        print("1. Log a habit")
        print("2. View progress")
        print("3. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            log_habit()
        elif choice == "2":
            result = view_progress()
            for habit_name, status_counts in result.items():
                print(f"{habit_name}: {status_counts['done']} done, {status_counts['missed']} missed")
        elif choice == "3":
            # TODO: figure out how to exit a while True loop
            break
            # hint: look up the "break" keyword
            pass
        else:
            print("Invalid option, try again.")
if __name__ == "__main__":
    main()