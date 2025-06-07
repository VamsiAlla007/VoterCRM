import csv
import pandas as pd
from sqlconnection import connection, cursor


# Read data from the CSV file into a DataFrame
csv_file = "voterCRM_sample_data.csv"
users_data = pd.read_csv(csv_file)

def create_table(table_name, columns):
    try: 
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} VARCHAR(255)' for col in columns])});"
        cursor.execute(create_table_query)
        connection.commit()
        print("Table creation successful")
    except Exception as err:
        print("Error in table creation: '{err}'")

# Insert data from a CSV file into a table
def insert_data_from_csv(csv_file, table_name):
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row if it exists in CSV file
        for row in csv_reader:
            # Define SQL INSERT statement
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
            cursor.execute(insert_query, tuple(row))
        print("Data insertion completed")
            

# Insert data into each table
insert_data_from_csv(csv_file, 'USERS')
insert_data_from_csv(csv_file, 'VOTER')
insert_data_from_csv(csv_file, 'ADDRESS')
insert_data_from_csv(csv_file, 'CONTACT')
insert_data_from_csv(csv_file, 'FAMILY')
insert_data_from_csv(csv_file, 'RELIGION')
insert_data_from_csv(csv_file, 'POLITICAL_AFFILIATION')
insert_data_from_csv(csv_file, 'POLICE_CASE')

# Commit the changes and close the connection
connection.commit()
connection.close()

if __name__ == "__main__":
    create_table('USERS', users_data.columns)
    create_table('VOTER', users_data.columns)
    create_table('ADDRESS', users_data.columns) 
    create_table('CONTACT', users_data.columns)
    create_table('FAMILY', users_data.columns)
    create_table('RELIGION', users_data.columns)
    create_table('POLITICAL_AFFILIATION', users_data.columns)
    create_table('POLICE_CASE', users_data.columns)
