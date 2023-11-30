import datetime
import sqlite3


class DatabaseHandler:
    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.create_table('''CREATE TABLE IF NOT EXISTS time_records (
                              id INTEGER PRIMARY KEY,
                              record_date TEXT,
                              start_time TEXT,
                              end_time TEXT,
                              task TEXT,
                              tag TEXT
                          )''')

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

    def create_new_record(self):
        try:
            date = input("Enter Date (YYYY/MM/DD): ")
            start_time = input("Enter Time from (HH:MM AM/PM): ")
            end_time = input("Enter Time to (HH:MM AM/PM): ")
            task = input("Enter Task: ")
            tag = input("Enter Tag: ")

            formatted_start_time = self.parse_and_format_time(start_time)
            formatted_end_time = self.parse_and_format_time(end_time)

            self.database_handler.execute_query(
                "INSERT INTO time_records (record_date, start_time, end_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                (date, formatted_start_time, formatted_end_time, task, tag)
            )

            print("Time recorded successfully!\n ")

        except ValueError as e:
            print(f"Error recording time: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

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
    QUERY_TYPES = {
        "1": DateQuery,
        "2": TaskQuery,
        "3": TagQuery,
    }

    def __init__(self, time_record_repository):
        self.time_record_repository = time_record_repository

    def query_records(self):
        print("Choose the type of query:\n")
        print("1. Date")
        print("2. Task")
        print("3. Tag")

        query_type_choice = input("Enter your choice (1, 2, or 3): ")

        if query_type_choice in self.QUERY_TYPES:
            query_class = self.QUERY_TYPES[query_type_choice]
            query_value = input(f"Enter the {query_class.__name__.replace('Query', '').lower()}: ")

            query = query_class(self.time_record_repository)
            query.execute_query(query_value)
        else:
            raise ValueError("Invalid choice for query type.")


class UserHandler:
    def __init__(self, time_record_app, query_handler):
        self.choice = ""
        self.time_record_app = time_record_app
        self.query_handler = query_handler

    def take_choice(self):
        print("What would you like to do?\n")
        print("Enter 1 to input information.")
        print("Enter 2 to search for information.")

        while True:
            task_to_do = input("Enter your choice 1 - 2: ")
            if task_to_do in ["1", "2"]:
                self.choice = task_to_do
                break
            else:
                print("Invalid choice. Please enter a valid option (1 or 2).")

        self.provide_options()

    def provide_options(self):
        options = {
            "1": self.time_record_app.create_new_record,
            "2": self.query_handler.query_records,
        }

        selected_option = options.get(self.choice)
        if selected_option:
            selected_option()
        else:
            print("Invalid choice. Returning to the main menu.")

    def run(self):
        while True:
            self.take_choice()


if __name__ == "__main__":
    connection_string = "time_records.db"
    db_handler = DatabaseHandler(connection_string)
    time_record_repository = TimeRecordRepository(db_handler)

    # Create an instance of QueryHandler
    query_handler = QueryHandler(time_record_repository)

    # Provide both time_record_app and query_handler to UserHandler
    time_record_app = UserHandler(time_record_repository, query_handler)
    time_record_app.run()
