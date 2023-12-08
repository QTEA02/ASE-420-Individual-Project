class QueryHandler:
    QUERY_TYPES = {
        "date": DateQuery,
        "task": TaskQuery,
        "tag": TagQuery,
    }

    def __init__(self, time_record_repository):
        self.time_record_repository = time_record_repository

    def query_records(self):
        print("Choose the type of query:\n")
        print("Date")
        print("Task")
        print("Tag")

        query_type_choice = input("Enter your choice (date, task, or tag): ")

        if query_type_choice.lower() in self.QUERY_TYPES:
            query_class = self.QUERY_TYPES[query_type_choice]
            query_value = input(f"Enter the {query_class.__name__.replace('Query', '').lower()}: ")

            query = query_class(self.time_record_repository)
            query.execute_query(query_value)
            return True
        else:
            raise ValueError("Invalid choice for query type.")
