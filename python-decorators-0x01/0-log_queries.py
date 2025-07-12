from datetime import datetime
import sqlite3
import functools

#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            query = args[0]
        else:
            query = None

        if query:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")