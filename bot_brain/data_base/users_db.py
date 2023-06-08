import sqlite3 as sql

location = 'users.db'

base = sql.connect(location)
cursor = base.cursor()


async def db_start():

    if base:
        print('Data base activated')
    base.execute('''CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    name TEXT,
    music INT,
    motive INT,
    weather INT
    )''')
    base.commit()


async def check_user_db(user_id):
    cursor.execute(f"""SELECT ROWID FROM users WHERE id = {user_id}""")
    return False if cursor.fetchone() is None else True


async def register_user_db(user_id, name):
    cursor.execute(f"""INSERT INTO users VALUES (?,?,?,?,?)""", (user_id, name, 0, 1, 1))
    base.commit()


async def get_all_user():
    cursor.execute("""SELECT id, name FROM users""")
    return cursor.fetchall()


async def delete_user(id_code):
    cursor.execute(f"""DELETE FROM users WHERE id={id_code}""")
    base.commit()


async def is_musician(user_id):
    cursor.execute(f"SELECT music FROM users WHERE id={user_id}")
    return False if cursor.fetchone()[0] == 1 else True
