import os
import sys
from unittest.mock import patch
from io import StringIO
import sqlite3
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from program import main # address later

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


def generate_test_input(*args):
    input_data = [str(item) for sublist in args for item in sublist]
    return iter(input_data)


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        (
                ["1", "2023-10-31", "12:30", "13:30", "Test Task", "Test Tag1"],
                "Data successfully inserted into the database."
        ),
        (
                ["1", "2023-11-30", "12:00", "13:10", "Test Task2", "Test Tag1"],
                "Data successfully inserted into the database."
        ),
        # Add more test cases as needed
    ]
)
@patch('builtins.input', side_effect=generate_test_input)
def test_main_data_input(mock_input, test_input, expected_output):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        clear_table("tasks", "tasks")

        main()

        output = fake_out.getvalue().strip()
        assert expected_output in output

        # Optionally, you can check the database for the inserted data and verify it matches the expected values.
        connection = sqlite3.connect("tasks")
        cursor = connection.cursor()
        records = cursor.execute("SELECT * FROM tasks").fetchall()
        connection.close()

        assert len(records) == 1, "Expected 1 record to be inserted."

        # Additional checks on the inserted data if needed
        # assert records[0] == expected_data_for_test_case

