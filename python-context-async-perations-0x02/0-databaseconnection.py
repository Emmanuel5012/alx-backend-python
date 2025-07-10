import mysql.connector

class DatabaseConnection:
    def __init__(self):
        # Initialize connection settings
        self.host = "localhost"
        self.user = "alx_prodev"
        self.password = ""
        self.database = "alx_prodev"
        self.port = 3306
        self.conn = None


    def __enter__(self):
        # Establish connection
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close connection
        if self.conn and self.conn.is_connected():
            self.conn.close()

if __name__ == "__main__":
    with DatabaseConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
        cursor.close()