import datetime
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("time_records.db")
cursor = conn.cursor()

# Drop the table if it exists
cursor.execute("DROP TABLE IF EXISTS time_records")
conn.commit()

# Create the table
cursor.execute('''CREATE TABLE time_records (
                    id INTEGER PRIMARY KEY,
                    record_date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    task TEXT,
                    tag TEXT
                )''')
conn.commit()

def record_time():
    try:
        date = input("Enter Date (YYYY/MM/DD): ")
        start_time = input("Enter Time from (HH:MM AM/PM): ")
        end_time = input("Enter Time to (HH:MM AM/PM): ")
        task = input("Enter Task: ")
        tag = input("Enter Tag: ")

        # Ensure the date format is correct
        date_format = "%Y/%m/%d"
        date = datetime.datetime.strptime(date, date_format).strftime(date_format)

        # Parse and format the start time
        start_time_parts = start_time.split()
        if len(start_time_parts) != 2:
            raise ValueError
        start_time_value = datetime.datetime.strptime(start_time_parts[0], "%I:%M")
        if start_time_parts[1].lower() == 'pm':
            start_time_value = start_time_value.replace(hour=start_time_value.hour + 12)
        start_time = start_time_value.strftime("%H:%M")

        # Parse and format the end time
        end_time_parts = end_time.split()
        if len(end_time_parts) != 2:
            raise ValueError
        end_time_value = datetime.datetime.strptime(end_time_parts[0], "%I:%M")
        if end_time_parts[1].lower() == 'pm':
            end_time_value = end_time_value.replace(hour=end_time_value.hour + 12)
        end_time = end_time_value.strftime("%H:%M")

        cursor.execute("INSERT INTO time_records (record_date, start_time, end_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                       (date, start_time, end_time, task, tag))
        conn.commit()
        print("Time recorded successfully!")
    except ValueError:
        print("Invalid input format. Please use the specified formats.")

def print_database():
    cursor.execute("SELECT * FROM time_records")
    records = cursor.fetchall()
    print("\nDatabase Contents:")
    for record in records:
        print(record)

while True:
    print("\n1. Record Time")
    print("2. Print Database Contents")
    print("3. Exit")
    choice = input("Select an option (1/2/3): ")

    if choice == "1":
        record_time()
    elif choice == "2":
        print_database()
    elif choice == "3":
        conn.close()
        break
    else:
        print("Invalid choice. Please select a valid option.")
