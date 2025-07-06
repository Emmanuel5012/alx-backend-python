import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows from user_data in batches."""
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

        while True:
            batch = cursor.fetchmany(batch_size)  # 👈 Fetch a batch of rows
            if not batch:
                break
            yield batch  # 👈 Yield the entire batch (list of rows)

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")


def batch_processing(batch_size):
    """Processes each batch and prints users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user[3] > 25:
                print(user)


if __name__ == "__main__":
    batch_processing(batch_size=5)
