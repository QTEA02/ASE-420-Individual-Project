README

Time Tracking App

A simple time-tracking application to record and query time records.

## Introduction
The Time Tracking App allows users to record and query time records. Users can create new records, and search for information based on date, task, or tag. 

It contains the following files:
- main (program.py)
- DatabaseHandler class which is responsible for creating the table and managing the session
- QueryHandler class which is responsible for managing query search
- TimeRecordRepository which is responsible for creating and storing new records
- UserHandler class which is responsible for handling user input

## Features
- Create new time records with date, start time, end time, task, and tag.
- Search for information based on date, task, or tag.
- Generate reports on date ranges and task priorities.

## Installation
1. Clone the repository: `git clone https://github.com/QTEA02/ASE420-Individual-Project.git`
3. Install dependencies: (List any dependencies or requirements)

## Usage
1. Run the application.
2. Choose an option:
   - Enter `1` to input information and create a new record.
   - Enter `2` to search for information based on date, task, or tag.

## Queries
- **Date Query:** Search for records based on a specific date.
- **Task Query:** Search for records based on a specific task.
- **Tag Query:** Search for records based on a specific tag.
