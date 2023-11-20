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
            self.time_record_repository.record_time(time_record)
            print("Time recorded successfully!")
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
