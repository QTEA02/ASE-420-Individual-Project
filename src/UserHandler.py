UserHandler.py:

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
            #changed to get-user_input
            "1": self.time_record_app.get_user_input,
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
