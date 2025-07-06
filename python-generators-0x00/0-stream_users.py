import mysql.connector

def stream_users():
    """Generator function that streams rows from user_data one at a time."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev",
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row  # ✅ Yield one row at a time (no more than one loop)

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")



if __name__ == "__main__":
    for user in stream_users():
        print(user)