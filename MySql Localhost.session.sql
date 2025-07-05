import mysql.connector
import csv
import uuid

def connect_to_prodev():
    """Connects to ALX_prodev database."""
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
        print(f"Connection error: {err}")
        return None