import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
    return rows  # ✅ Added return

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
    return rows  # ✅ Added return

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n📦 All Users:")
    for row in users:
        print(row)

    print("\n🎯 Users Older Than 40:")
    for row in older_users:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
