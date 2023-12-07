import datetime

class TimeRecordRepository:
    def __init__(self, database_handler):
        self.database_handler = database_handler
        # added
        self.date = ""
        self.start_time = ""
        self.end_time = ""
        self.task = ""
        self.tag = ""
        self.formatted_start_time = ""
        self.formatted_end_time = ""

    # added
    def get_user_input(self):
        self.date = input("Enter Date (YYYY/MM/DD): ")
        self.start_time = input("Enter Time from (HH:MM AM/PM): ")
        self.end_time = input("Enter Time to (HH:MM AM/PM): ")
        self.task = input("Enter Task: ")
        self.tag = input("Enter Tag: ")

        self.formatted_start_time = self.parse_and_format_time(self.start_time)
        self.formatted_end_time = self.parse_and_format_time(self.end_time)

        self.create_new_record()

    # remove user input gathering function to another method
    def create_new_record(self):
        try:
            #added self
            self.database_handler.execute_query(
                "INSERT INTO time_records (record_date, start_time, end_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                (self.date, self.formatted_start_time, self.formatted_end_time, self.task, self.tag)
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
