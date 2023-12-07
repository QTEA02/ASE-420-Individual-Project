from src.DatabaseHandler import DatabaseHandler
from src.TimeRecordRepository import TimeRecordRepository
from src.QueryHandler import QueryHandler
from src.UserHandler import UserHandler


def main():
    connection_string = "time_records.db"
    db_handler = DatabaseHandler(connection_string)
    time_record_repository = TimeRecordRepository(db_handler)

    # Create an instance of QueryHandler
    query_handler = QueryHandler(time_record_repository)

    # Provide both time_record_app and query_handler to UserHandler
    time_record_app = UserHandler(time_record_repository, query_handler)
    time_record_app.run()


if __name__ == "__main__":
    main()
