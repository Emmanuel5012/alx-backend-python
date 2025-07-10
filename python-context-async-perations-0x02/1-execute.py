import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params=None):
        # Initialize with query parameters
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None


    def __enter__(self):
        # Establish connection and execute the query
        self.connection = mysql.connector.connect(
            host="localhost",
            user="alx_prodev",
            password="",
            database="alx_prodev",
            port=3306
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall() #Returns query results


    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM users WHERE age > %s", (25,)) as results:
        for row in results:
            print(row)