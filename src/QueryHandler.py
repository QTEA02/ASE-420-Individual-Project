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
            return True
        else:
            raise ValueError("Invalid choice for query type.")

