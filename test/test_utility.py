import os
import sys
from unittest.mock import patch
from io import StringIO
import sqlite3
import pytest
from unittest.mock import patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from program import main
from program import DatabaseHandler
from program import TimeRecordRepository
from program import Query
from program import DateQuery
from program import TaskQuery
from program import TagQuery
from program import QueryHandler
from program import UserHandler



def clear_table(db_name, table_name):
    connection = sqlite3.connect(db_name)

    try:
        cursor = connection.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

@pytest.fixture
def setup_fixture(scope="session"):
    connection_string = "time_records.db"
    data_handler = DatabaseHandler(connection_string)
    clear_table(connection_string, "test_time_records")  # Use the same table name as in your test

    time_record_repository = TimeRecordRepository(data_handler)
    date_query = DateQuery(time_record_repository)
    task_query = TaskQuery(time_record_repository)
    tag_query = TagQuery(time_record_repository)
    query_handler = QueryHandler(time_record_repository)
    user_handler = UserHandler(time_record_repository, query_handler)

    objList = [data_handler, time_record_repository, date_query, task_query,
               tag_query, query_handler, user_handler]

    return objList  # You can return any other objects you want to use in your tests

def test_create_table(setup_fixture):
    
    connection = setup_fixture[0].conn
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS test_time_records')
    connection.commit()

    # Query the sqlite_master table to check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='test_time_records'")
    result = cursor.fetchone()
    results = result is None
    assert results

    setup_fixture[0].create_table('''CREATE TABLE IF NOT EXISTS test_time_records (
                              id INTEGER PRIMARY KEY,
                              record_date TEXT,
                              start_time TEXT,
                              end_time TEXT,
                              task TEXT,
                              tag TEXT
                          )''') 
    
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='test_time_records'")
    result = cursor.fetchone()
    connection.close()

    results = result is not None
    assert results

def test_execute_query(setup_fixture):
    date = "2023-12-01"
    formatted_start_time = "09:00 AM"
    formatted_end_time = "12:00 PM"
    task = "Sample Task"
    tag = "Sample Tag"
    
    query = "INSERT INTO time_records (record_date, start_time, end_time, task, tag) VALUES (?, ?, ?, ?, ?)"
    parameters = (date, formatted_start_time, formatted_end_time, task, tag)
    
    query2 = "SELECT * FROM time_records WHERE task = 'Sample Task'"

    assert setup_fixture[0].execute_query(query, parameters)
    assert setup_fixture[0].execute_query(query2)

def test_fetch_all(setup_fixture):

    task = ("Sample Task",)
    query = "SELECT * FROM time_records WHERE task = ?"
    query2 = "SELECT * FROM time_records WHERE task = 'Sample Task'"
    
    assert setup_fixture[0].execute_query(query, task)
    assert setup_fixture[0].execute_query(query2)

def test_get_user_input(setup_fixture, monkeypatch):

    user_input_values = [
        "2023/12/01",  # Date
        "09:00 AM",    # Start Time
        "12:00 PM",    # End Time
        "Sample Task", # Task
        "Sample Tag"   # Tag
    ]

    def mock_input(prompt):
        return user_input_values.pop(0)

    # Apply the mock_input function to replace the built-in input function
    monkeypatch.setattr('builtins.input', mock_input)

    # Create an instance of your class (replace YourClass with the actual class name)
    instance = TimeRecordRepository(setup_fixture[0])

    # Call the method to test
    instance.get_user_input()

    # Check that the instance attributes are set correctly
    assert instance.date == "2023/12/01"
    assert instance.start_time == "09:00 AM"
    assert instance.end_time == "12:00 PM"
    assert instance.task == "Sample Task"
    assert instance.tag == "Sample Tag"

def test_create_new_record(setup_fixture):

    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    setup_fixture[1].date = "2023-10-01"
    setup_fixture[1].formatted_start_time = "10:00"
    setup_fixture[1].formatted_end_time = "23:00"
    setup_fixture[1].task = "Sample Task2"
    setup_fixture[1].tag = "Sample Tag2"

    setup_fixture[1].create_new_record()

    query = "SELECT * FROM time_records WHERE task = 'Sample Task2'"
    cursor.execute(query)
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == "2023-10-01"
    assert result[2] == "10:00"
    assert result[3] == "23:00"
    assert result[4] == "Sample Task2"
    assert result[5] == "Sample Tag2"


    

