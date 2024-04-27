import csv
import json
import mysql.connector

with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Clear the table
truncate_stmt = "TRUNCATE TABLE stories"
cursor.execute(truncate_stmt)

insert_stmt = (
    "INSERT INTO stories (story_name, surface_story, truth) "
    "VALUES (%s, %s, %s)"
)

# Read and insert new data from CSV
with open('story_database/new_stories.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        cursor.execute(insert_stmt, row)

# Commit changes and close connection
db_connection.commit()
cursor.close()
db_connection.close()



''' #checking if there are three elements as expected
import csv

def clean_row(row):
    return [item.replace('"', '').replace("'", "") for item in row]

with open('story_database/story_table.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row_number, row in enumerate(csvreader, start=2):  # Start from 2 assuming first row is the header
        if len(row) != 3:
            print(f"Row {row_number} is malformed: {row}")
        cleaned_row = clean_row(row)
        print(f"Row {row_number} cleaned: {cleaned_row}")

'''