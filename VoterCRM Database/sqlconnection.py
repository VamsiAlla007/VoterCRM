import mysql.connector
from VoterCRM_database import *

# Database connection parameters
user = "root"
host = "127.0.0.1"
password = "streamlit"
database = "VOTER_DATA"

# Establish a database connection
def create_server_connection(host_name, user_name, user_password):
        try:
            connection = mysql.connector.connect (
                    host=host_name,
                    user=user_name,
                    passwd=user_password,
                    auth_plugin = 'mysql_native_password'
                )
            print("MySQL database connection successful")
            return connection
        except Exception as err:
            print(f"Failed to establish a database connection: {err}")
            return None

        
def create_and_switch_database(connection, database_name):
    cursor = connection.cursor()
    try:
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        use_db_query = f"USE {database_name}"
        cursor.execute(create_db_query)
        cursor.execute(use_db_query)
        print(" Database created and switched successfully")
    except Exception as err:
        print("Error in creating or switching database: {err}")


def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")

if __name__ == "__main__":
    connection = create_server_connection(host, user, password)

    if connection is not None:
       create_and_switch_database(connection, database)
       cursor = connection.cursor()
    else:
       print("Connection to the database was not successful. Check your connection parameters and make sure the database server is running.")


