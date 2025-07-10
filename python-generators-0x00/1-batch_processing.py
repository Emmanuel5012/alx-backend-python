import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows from user_data in batches."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_prodev",
            password="",
            database="alx_prodev",
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
    """Processes each batch and returns users over the age of 25."""
    filtered_users = []
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user[3] > 25:
                filtered_users.append(user)

    return filtered_users


if __name__ == "__main__":
   users = batch_processing(5)
   for user in users:
       print(user)
