import mysql.connector

class DatabaseConnection:
    def __enter__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="alx_prodev",
            password="",
            database="alx_prodev",
            port=3306
        )

        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn.is_connected():
            self.conn.close()

if __name__ == "__main__":
    with DatabaseConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        results = cursor.fetchall()
        for row in results:
            print(row)
        cursor.close()