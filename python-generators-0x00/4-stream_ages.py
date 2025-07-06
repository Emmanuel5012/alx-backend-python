import mysql.connector

def stream_user_ages():
    """Generator that yields one user age at a time from the user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev",
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # row is a tuple like (age,), so we yield row[0]

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")


def compute_average_age():
    """Calculates the average age using a generator."""
    total = 0
    count = 0

    for age in stream_user_ages():  #  First loop
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"✅ Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()
