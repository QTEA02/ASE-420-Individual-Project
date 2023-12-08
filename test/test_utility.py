import os
import sys
from unittest.mock import patch
from io import StringIO
import sqlite3
import pytest
from unittest.mock import patch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from program import main
from DatabaseHandler import DatabaseHandler
from TimeRecordRepository import TimeRecordRepository
from QueryHandler import DateQuery
from QueryHandler import TaskQuery
from QueryHandler import TagQuery
from QueryHandler import QueryHandler
from UserHandler import UserHandler



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

    monkeypatch.setattr('builtins.input', mock_input)

    instance = setup_fixture[6]
   
    instance.get_user_input()

    assert instance.date == "2023/12/01"
    assert instance.start_time == "09:00"
    assert instance.end_time == "12:00"
    assert instance.task == "Sample Task"
    assert instance.tag == "Sample Tag"

def test_create_new_record(setup_fixture):

    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    date = "2023-10-01"
    start_time = "10:00"
    end_time = "23:00"
    task = "Sample Task2"
    tag = "Sample Tag2"

    setup_fixture[1].create_new_record(date, start_time, end_time, task, tag)

    query = "SELECT * FROM time_records WHERE task = 'Sample Task2'"
    cursor.execute(query)
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == "2023-10-01"
    assert result[2] == "10:00"
    assert result[3] == "23:00"
    assert result[4] == "Sample Task2"
    assert result[5] == "Sample Tag2"

def test_parse_and_format_time(setup_fixture):  
   
    results = setup_fixture[6].parse_and_format_time("10:00 PM")
    assert results == "22:00"

    results = setup_fixture[6].parse_and_format_time("10:00 AM")
    assert results == "10:00"

def test_DateQuery_execute_query(setup_fixture, capsys):
   
    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    date = "2023/10/01"
    start_time = "10:00"
    end_time = "23:00"
    task = "Sample Task2"
    tag = "Sample Tag2"

    setup_fixture[1].create_new_record(date, start_time, end_time, task, tag)

    setup_fixture[2].execute_query('2023/10/01')
    captured = capsys.readouterr()
    assert '2023/10/01' in captured.out
   
    setup_fixture[2].execute_query('2022/10/01')
    captured = capsys.readouterr()
    assert 'No records found' in captured.out

def test_TaskQuery_execute_query(setup_fixture, capsys):
   
    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    date = "2023/10/01"
    start_time = "10:00"
    end_time = "23:00"
    task = "Sample Task2"
    tag = "Sample Tag2"

    setup_fixture[1].create_new_record(date, start_time, end_time, task, tag)

    setup_fixture[3].execute_query('Sample Task2')
    captured = capsys.readouterr()
    assert 'Sample Task2' in captured.out
   
    setup_fixture[3].execute_query('Sample Task3')
    captured = capsys.readouterr()
    assert 'No records found' in captured.out

def test_TagQuery_execute_query(setup_fixture, capsys):
   
    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    date = "2023/10/01"
    start_time = "10:00"
    end_time = "23:00"
    task = "Sample Task2"
    tag = "Sample Tag2"

    setup_fixture[1].create_new_record(date, start_time, end_time, task, tag)

    setup_fixture[4].execute_query('Sample Tag2')
    captured = capsys.readouterr()
    assert 'Sample Tag2' in captured.out
   
    setup_fixture[4].execute_query('Sample Tag3')
    captured = capsys.readouterr()
    assert 'No records found' in captured.out

def test_query_records(setup_fixture, monkeypatch):

    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    date = "2023/10/01"
    start_time = "10:00"
    end_time = "23:00"
    task = "Sample Task2"
    tag = "Sample Tag2"

    setup_fixture[1].create_new_record(date, start_time, end_time, task, tag)
   
    user_input_values = [
        "task",
        "Sample Task2",
    ]

    def mock_input(prompt):
        return user_input_values.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)

    instance = setup_fixture[5]
   
    assert instance.query_records()

def test_take_choice(setup_fixture, monkeypatch, capsys):

    connection = setup_fixture[0].conn
    cursor = connection.cursor()

    cursor.execute(f'DELETE FROM time_records')

    date = "2023/10/01"
    start_time = "10:00"
    end_time = "23:00"
    task = "Sample Task2"
    tag = "Sample Tag2"

    setup_fixture[1].create_new_record(date, start_time, end_time, task, tag)

    user_input_values = [
        "2",
        "task",
        "Sample Task2",
    ]

    def mock_input(prompt):
        return user_input_values.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)

    instance = setup_fixture[6]

    instance.take_choice()

    captured = capsys.readouterr()

    assert "Sample Task2" in captured.out
