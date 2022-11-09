import sqlite3 as sql

location = 'users.db'


async def db_start():
    base = sql.connect(location)
    if base:
        print('Data base activated')
    base.execute('''CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    name TEXT
    )''')
    base.commit()


async def check_user_db(user_id):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""SELECT ROWID FROM users WHERE id = {user_id}""")
    return False if cursor.fetchone() is None else True


async def register_user_db(user_id, name):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""INSERT INTO users VALUES (?,?)""", (user_id, name))
    base.commit()


async def get_all_user():
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute("""SELECT id, name FROM users""")
    return cursor.fetchall()


async def delete_user(id_code):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""DELETE FROM users WHERE id={id_code}""")
    base.commit()
