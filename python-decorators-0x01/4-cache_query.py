import time
import sqlite3
import functools

query_cache = {}

### Decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

### Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None

        if query in query_cache:
            print("[CACHE] Returning cached result for query.")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[DB] Query executed and result cached.")
        return result
    return wrapper

@cache_query
@with_db_connection
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
