import datetime

class UserHandler:
    def __init__(self, query_handler):
        self.choice = ""
        self.query_handler = query_handler
        self.date = ""
        self.start_time = ""
        self.end_time = ""
        self.task = ""
        self.tag = ""

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

        options = {
            #changed to get-user_input
            "1": self.get_user_input,
            "2": self.query_handler.query_records,
        }

        selected_option = options.get(self.choice)
        if selected_option:
            selected_option()
        else:
            print("Invalid choice. Returning to the main menu.")

    def run(self):
        #while True: #delete
            self.take_choice()

    def get_user_input(self):
        self.date = input("Enter Date (YYYY/MM/DD): ")
        self.start_time = input("Enter Time from (HH:MM AM/PM): ")
        self.end_time = input("Enter Time to (HH:MM AM/PM): ")
        self.task = input("Enter Task: ")
        self.tag = input("Enter Tag: ")

        self.start_time = self.parse_and_format_time(self.start_time)
        self.end_time = self.parse_and_format_time(self.end_time)

        try:
            self.time_record_app.create_new_record(self.date, self.start_time, self.end_time, self.task, self.tag)
            print("Time recorded successfully!\n ")
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
