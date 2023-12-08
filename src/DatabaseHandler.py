import sqlite3

class DatabaseHandler:
    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.build_query = []
        self.success = False
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
        try:
            self.build_query.append(query)
            self.build_query.append(parameters)
            self.cursor.execute(*self.build_query)
            self.conn.commit()
            self.succcess = True
        except sqlite3.Error as e:
            print("Error during commit:", e)
            self.conn.close()
        finally:
            return self.succcess
       
    def fetch_all(self, query, parameters):
       
        try:
            self.build_query.clear()
            self.build_query.append(query)
            self.build_query.append(parameters)
            print(self.build_query)
            self.cursor.execute(*self.build_query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error during commit:", e)
            self.conn.close()

    def close_connection(self):
        self.conn.close()
