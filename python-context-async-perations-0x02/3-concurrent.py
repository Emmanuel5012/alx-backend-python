import aiosqlite
import asyncio

# Async function to fetch all users
async def async_fetch_users():
    # Connect to the SQLite database
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            # Fetch all rows from the last executed statement
            rows = await cursor.fetchall()
            print("\n All Users:")
            for row in rows:
                print(row)

# Async function to fetch users older than 40
async def async_fetch_older_users():
    # Connect to the SQLite database
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            # Fetch all rows from the last executed statement
            rows = await cursor.fetchall()
            print("\n Users Older Than 40:")
            for row in rows:
                print(row)
            
# Run both at the same time
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(), 
        async_fetch_older_users()
        )
    
# Run the async program
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())