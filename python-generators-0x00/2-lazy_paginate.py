import mysql.connector

def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_prodev",
            password="",
            database="alx_prodev",
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []


def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for user in page:
            yield user
        offset += page_size


if __name__ == "__main__":
    for user in lazy_paginate(5):
        print(user)
