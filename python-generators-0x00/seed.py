"""This module connects to MySQL and streams user data from a CSV file."""

import csv
import mysql.connector


def connect_db():
    """Connects to the MySQL server (not a specific database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        
            password="",        
            port=3306
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it doesn't already exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
        print("✅ Database 'ALX_prodev' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Database creation error: {err}")


def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev",
            port=3306
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection to ALX_prodev failed: {err}")
        return None


def create_table(connection):
    """Creates the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()
    print("✅ Table 'user_data' created or already exists.")


import uuid

def insert_data(connection, user_data="user_data.csv"):
    """Inserts users from a CSV file into the user_data table."""
    cursor = connection.cursor()

    try:
        with open(user_data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Generate a new UUID for the user
                user_id = str(uuid.uuid4())

                # Optional: Check if email already exists to avoid duplicates
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (row['email'],))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        user_id,
                        row['name'],
                        row['email'],
                        row['age']
                    ))

        connection.commit()
        print("✅ Data inserted from CSV.")
    except FileNotFoundError:
        print(f"❌ File '{user_data}' not found.")
    except Exception as e:
        print(f"❌ Error reading CSV or inserting data: {e}")
    finally:
        cursor.close()

    # Inserts users from a CSV file into the user_data table.
    cursor = connection.cursor()

    try:
        with open(user_data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if the user already exists to avoid duplicates
                cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (row['user_id'],))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        row['user_id'],
                        row['name'],
                        row['email'],
                        row['age']
                    ))

        connection.commit()
        print("✅ Data inserted from CSV.")
    except FileNotFoundError:
        print(f"❌ File '{user_data}' not found.")
    except Exception as e:
        print(f"❌ Error reading CSV or inserting data: {e}")
    finally:
        cursor.close()


# def stream_users(connection):
#     """Generator that streams users from the database one by one."""
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM user_data")
#     while True:
#         row = cursor.fetchone()
#         if row is None:
#             break
#         yield row
#     cursor.close()
