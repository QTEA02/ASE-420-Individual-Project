import sqlite3

class DatabaseHandler:
    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cursor = self.conn.cursor()
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

   
    # can be removed by using a list, and appending query and parameters if you have them.
    # ex add query to list. IF parameters, add parameters to list
    # after that you can use a spread operator with the execute() to input add args.
    def execute_query(self, query, parameters=None):
        if parameters is not None:
            self.cursor.execute(query, parameters)
            self.conn.commit()
            return True
        elif parameters is None:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        else:
            return False 
       
       
    # can be removed by using a list, and appending query and parmeters if you have them.
    # ex add query to list. IF parameters, add parameters to list
    # after that you can use a spread operator with the execute() to input add args.
    def fetch_all(self, query, parameters=None):
        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
