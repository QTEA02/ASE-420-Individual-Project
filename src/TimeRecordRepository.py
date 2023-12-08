class TimeRecordRepository:
    def __init__(self, database_handler):
        self.database_handler = database_handler
        self.date = ""
        self.start_time = ""
        self.end_time = ""
        self.task = ""
        self.tag = ""


    def create_new_record(self, date, start_time, end_time, task, tag):
        self.date = date
        self.formatted_start_time = start_time
        self.formatted_end_time = end_time
        self.task = task
        self.tag = tag
        self.database_handler.execute_query(
            "INSERT INTO time_records (record_date, start_time, end_time, task, tag) VALUES (?, ?, ?, ?, ?)",
            (self.date, self.formatted_start_time, self.formatted_end_time, self.task, self.tag)
        )
