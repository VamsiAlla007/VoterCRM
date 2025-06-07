# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pymysql.cursors
import pandas as pd

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Add your authentication logic here
        if username == "your_username" and password == "your_password":
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials.")
# Function to connect to MySQL database and fetch data
def fetch_data_from_mysql(host, user, password, database, query):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
    finally:
        connection.close()

    return df

def main():
    st.title("MySQL Data Viewer")

    # User input for MySQL connection details
    host = st.text_input("Enter MySQL Host", "localhost")
    user = st.text_input("Enter MySQL User", "root")
    password = st.text_input("Enter MySQL Password", "", type="password")
    database = st.text_input("Enter MySQL Database", "your_database_name")

    # User input for SQL query
    query = st.text_area("Enter SQL Query", "SELECT * FROM your_table_name")

    # Automatically fetch data when the app is loaded
    if st.experimental_get_query_params():
        st.experimental_run_once()

        # Call the function to connect to MySQL and fetch data
        df = fetch_data_from_mysql(host, user, password, database, query)

        # Display the fetched data
        st.write(df)
    st.title("Login Page")
    login()

if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
