import datetime
import sqlite3


class DatabaseHandler:
    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()

    def create_table(self, table_creation_query):
        self.cursor.execute(table_creation_query)
        self.conn.commit()

    def execute_query(self, query, parameters=None):
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_all(self, query, parameters=None):
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()


class TimeRecord:
    def __init__(self, date, start_time, end_time, task, tag):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.task = task
        self.tag = tag

    @staticmethod
    def parse_and_format_time(time_str):
        try:
            time_parts = time_str.split()
            if len(time_parts) != 2:
                raise ValueError("Invalid time format")

            time_value = datetime.datetime.strptime(time_parts[0], "%I:%M")
            if time_parts[1].lower() == 'pm':
                time_value = time_value.replace(hour=time_value.hour + 12)

            return time_value.strftime("%H:%M")

        except ValueError as e:
            raise ValueError(f"Error parsing time: {str(e)}")


class TimeRecordRepository:
    def __init__(self, database_handler):
        self.database_handler = database_handler

    def create_table(self):
        self.database_handler.create_table('''CREATE TABLE IF NOT EXISTS time_records (
                                              id INTEGER PRIMARY KEY,
                                              record_date TEXT,
                                              start_time TEXT,
                                              end_time TEXT,
                                              task TEXT,
                                              tag TEXT
                                          )''')

    def record_time(self, time_record):
        try:
            formatted_start_time = TimeRecord.parse_and_format_time(time_record.start_time)
            formatted_end_time = TimeRecord.parse_and_format_time(time_record.end_time)

            self.database_handler.execute_query(
                "INSERT INTO time_records (record_date, start_time, end_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                (time_record.date, formatted_start_time, formatted_end_time, time_record.task, time_record.tag)
            )

            return "Time recorded successfully!"
        except ValueError as e:
            return f"Error recording time: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def print_database(self):
        records = self.database_handler.fetch_all("SELECT * FROM time_records")
        print("\nDatabase Contents:")
        for record in records:
            print(record)


class Query:
    def __init__(self, time_record_repository):
        self.time_record_repository = time_record_repository

    def execute_query(self, query_value):
        pass


class DateQuery(Query):
    def execute_query(self, query_value):
        records = self.time_record_repository.database_handler.fetch_all(
            "SELECT * FROM time_records WHERE record_date = ?", (query_value,)
        )
        self.display_results(records)

    def display_results(self, records):
        if not records:
            print(f"No records found.")
        else:
            print(f"\nQuery Results:")
            for record in records:
                print(record)


class TaskQuery(Query):
    def execute_query(self, query_value):
        records = self.time_record_repository.database_handler.fetch_all(
            "SELECT * FROM time_records WHERE task = ?", (query_value,)
        )
        self.display_results(records)

    def display_results(self, records):
        if not records:
            print(f"No records found.")
        else:
            print(f"\nQuery Results:")
            for record in records:
                print(record)


class TagQuery(Query):
    def execute_query(self, query_value):
        records = self.time_record_repository.database_handler.fetch_all(
            "SELECT * FROM time_records WHERE tag = ?", (query_value,)
        )
        self.display_results(records)

    def display_results(self, records):
        if not records:
            print(f"No records found.")
        else:
            print(f"\nQuery Results:")
            for record in records:
                print(record)


class QueryHandler:
    def __init__(self, time_record_repository):
        self.time_record_repository = time_record_repository

    def query_records(self, query_type, query_value):
        query = self.create_query(query_type)
        query.execute_query(query_value)

    def create_query(self, query_type):
        if query_type == "date":
            return DateQuery(self.time_record_repository)
        elif query_type == "task":
            return TaskQuery(self.time_record_repository)
        elif query_type == "tag":
            return TagQuery(self.time_record_repository)
        else:
            raise ValueError("Invalid query type. Please use 'date', 'task', or 'tag'.")


class InputHandler:
    @staticmethod
    def get_user_input(prompt, input_type=str):
        while True:
            try:
                user_input = input(prompt)
                return input_type(user_input)
            except ValueError:
                print("Invalid input. Please try again.")


class TimeRecordApp:
    def __init__(self, time_record_repository, input_handler, query_handler):
        self.time_record_repository = time_record_repository
        self.input_handler = input_handler
        self.query_handler = query_handler

    def run(self):
        self.time_record_repository.create_table()

        while True:
            self.print_menu()
            choice = self.input_handler.get_user_input("Select an option (1/2/3/4): ", str)

            if choice == "1":
                self.record_time()
            elif choice == "2":
                self.print_database()
            elif choice == "3":
                self.query_records_menu()
            elif choice == "4":
                self.shutdown()
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def print_menu(self):
        print("\n1. Record Time")
        print("2. Print Database Contents")
        print("3. Query Records")
        print("4. Exit")

    def record_time(self):
        try:
            date = self.input_handler.get_user_input("Enter Date (YYYY/MM/DD): ", str)
            start_time = self.input_handler.get_user_input("Enter Time from (HH:MM AM/PM): ", str)
            end_time = self.input_handler.get_user_input("Enter Time to (HH:MM AM/PM): ", str)
            task = self.input_handler.get_user_input("Enter Task: ", str)
            tag = self.input_handler.get_user_input("Enter Tag: ", str)

            time_record = TimeRecord(date, start_time, end_time, task, tag)
            result_message = self.time_record_repository.record_time(time_record)
            print(result_message)
        except ValueError as e:
            print(f"Error recording time: {str(e)}")

    def print_database(self):
        try:
            self.time_record_repository.print_database()
        except Exception as e:
            print(f"Error fetching database records: {str(e)}")

    def query_records_menu(self):
        print("\nQuery Options:")
        print("1. Query by Date")
        print("2. Query by Task")
        print("3. Query by Tag")
        print("4. Back to Main Menu")

        query_choice = self.input_handler.get_user_input("Select an option (1/2/3/4): ", str)

        if query_choice == "1":
            self.query_records("date", self.input_handler.get_user_input("Enter Date (YYYY/MM/DD): ", str))
        elif query_choice == "2":
            self.query_records("task", self.input_handler.get_user_input("Enter Task: ", str))
        elif query_choice == "3":
            self.query_records("tag", self.input_handler.get_user_input("Enter Tag: ", str))
        elif query_choice == "4":
            pass  # Back to the main menu
        else:
            print("Invalid choice. Returning to the main menu.")

    def query_records(self, query_type, query_value):
        self.query_handler.query_records(query_type, query_value)

    def shutdown(self):
        try:
            self.time_record_repository.database_handler.close_connection()
            print("Exiting the application. Goodbye!")
        except Exception as e:
            print(f"Error closing the database connection: {str(e)}")


# Example usage:
if __name__ == "__main__":
    connection_string = "time_records.db"
    table_creation_query = '''CREATE TABLE IF NOT EXISTS time_records (
                                id INTEGER PRIMARY KEY,
                                record_date TEXT,
                                start_time TEXT,
                                end_time TEXT,
                                task TEXT,
                                tag TEXT
                            )'''

    database_handler = DatabaseHandler(connection_string)
    database_handler.create_table(table_creation_query)

    time_record_repository = TimeRecordRepository(database_handler)
    input_handler = InputHandler()
    query_handler = QueryHandler(time_record_repository)
    time_record_app = TimeRecordApp(time_record_repository, input_handler, query_handler)

    time_record_app.run()
