import re

def validate_date_range_format(input_string):
    # Define the regular expression pattern
    pattern = r'^\d{4}/\d{2}/\d{2}-\d{4}/\d{2}/\d{2}$'

    # Use re.match() to check if the input string matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False

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

class DateRange(Query):
    def execute_query(self, query_value):
        valueList = query_value.split('-')
        records = self.time_record_repository.database_handler.fetch_all(
            "SELECT * FROM time_records WHERE record_date BETWEEN ? AND ?", tuple(valueList)
        )
        self.display_results(records)

    def display_results(self, records):
        if not records:
            print(f"No records found.")
        else:
            print(f"\nReport Results:")
            for record in records:
                print(record)

class Priority(Query):

    def execute_query(self):
        records = self.time_record_repository.database_handler.fetch_all(
            '''SELECT tag,
               SUM(strftime('%s', end_time) - strftime('%s', start_time)) AS total_duration
        FROM time_records
        GROUP BY tag
        ORDER BY total_duration DESC''',()
        )
        self.display_results(records)

    def display_results(self, records):
        if not records:
            print(f"No records found.")
        else:
            print(f"\nReport results:")
            print(f"(Task Tag, Time in minutes)")
            for record in records:
                outList = [*record]
                outList[1] = abs(int(record[1]) // 60)
                print(outList)

class QueryHandler:
    QUERY_TYPES = {
        "date": DateQuery,
        "task": TaskQuery,
        "tag": TagQuery,
    }

    REPORT_TYPES = {
        "range": DateRange,
        "priority": Priority
    }

    def __init__(self, time_record_repository):
        self.time_record_repository = time_record_repository

    def query_records(self):
        print("Choose the type of query:\n")
        print("Date")
        print("Task")
        print("Tag")
        print("Date Range")
        print("Priority")

        query_type_choice = input("Enter your choice (date, task, tag, range, priority): ")

        if query_type_choice.lower() in self.QUERY_TYPES:
            query_class = self.QUERY_TYPES[query_type_choice]
            query_value = input(f"Enter the {query_class.__name__.replace('Query', '').lower()}: ")

            query = query_class(self.time_record_repository)
            query.execute_query(query_value)
            return True
        elif query_type_choice.lower() in self.REPORT_TYPES:
            query_class = self.REPORT_TYPES[query_type_choice]

            if query_type_choice.lower() == "range":
                query_value = input(f"Enter the date range (YYYY/MM/DD-YYYY/MM/DD)")
                
                while not validate_date_range_format(query_value):
                    print("Invalid date range")
                    query_value = input(f"Enter the date range (YYYY/MM/DD-YYYY/MM/DD)")

                query = query_class(self.time_record_repository)
                query.execute_query(query_value)
                return True
            else:
                query = query_class(self.time_record_repository)
                query.execute_query()
                return True
        else:
            raise ValueError("Invalid choice for query type.")
