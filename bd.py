import sqlite3


#####################################################################
"""STUDLIFE JOB"""
def get_id_job():
    try:
        conn = sqlite3.connect("job.db")
        cur = conn.cursor()

        cur.execute("SELECT id FROM resume")
        count = cur.fetchall()

        conn.commit()

        print("[DEBUG] Данные id получены")
        print()

        return count

    except Exception as e:
        print(e)


def get_resume(id):
    try:
        conn = sqlite3.connect("job.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM resume WHERE id = ?", (id,))
        count = cur.fetchone()
        print(count)

        conn.commit()

        print("[DEBUG] Данные полученны из mate")
        print(count)
        print()

        if count:
            return count
        else:
            return [None] * 5

    except Exception as e:
        print(e)


def register_resume(id, name, username, address, desc_yourself):
    try:
        conn = sqlite3.connect("job.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM resume WHERE id = ?", (id,))
        count = cur.fetchone()


        if count:
            sql = "UPDATE resume SET name = ?, username = ?, address = ?, desc_yourself = ? WHERE id = ?"
            cur.execute(sql, (name, username, address, desc_yourself, id))
        else:
            sql = "INSERT INTO resume (id, name, username, address, desc_yourself) VALUES (?, ?, ?, ?, ?)"
            cur.execute(sql, (id, name, username, address, desc_yourself))

        conn.commit()

        print("[DEBUG] Данные добавлены")
        print(
            f"id={id}, name={name}")
        print()

    except Exception as e:
        print(e)


def feed_job(address):
    try:
        conn = sqlite3.connect("job.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM vacancy WHERE address = ?",
                    (address, ))
        count = cur.fetchall()

        conn.commit()

        print("[DEBUG] Данные получены из таблицы vacancy")
        print()

        return count

    except Exception as e:
        print(e)

def del_job(id, is_on):
    try:
        conn = sqlite3.connect("job.db")
        cur = conn.cursor()

        cur.execute("UPDATE vacancy SET is_on = ? WHERE id = ?", (is_on, id,))

        conn.commit()

        print(f"[DEBUG] запись удалена {id=}")

    except Exception as e:
        print(e)

def register_job(name, address, post, responsibilities, requirements, conditions, salary):
    try:
        conn = sqlite3.connect("job.db")
        cur = conn.cursor()

        sql = "INSERT INTO vacancy (name, address, post, responsibilities, requirements, conditions, salary, is_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(sql, (name, address, post, responsibilities, requirements, conditions, salary, 1))

        conn.commit()

        print("[DEBUG] Данные добавлены")
        print(
            f"name={name}, post={post}")
        print()

    except Exception as e:
        print(e)


#####################################################################
"""STUDLIFE MATE"""

def get_id_mate():
    try:
        conn = sqlite3.connect("mate.db")
        cur = conn.cursor()

        cur.execute("SELECT id FROM mate")
        count = cur.fetchall()

        conn.commit()

        print("[DEBUG] Данные id получены")
        print()

        return count

    except Exception as e:
        print(e)


def get_mate(id):
    try:
        conn = sqlite3.connect("mate.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM mate WHERE id = ?", (id,))
        count = cur.fetchone()
        print(count)

        conn.commit()

        print("[DEBUG] Данные полученны из mate")
        print(count)
        print()

        if count:
            return count
        else:
            return [None] * 10

    except Exception as e:
        print(e)


def register_mate(id, name, username, address, age, price, sex_mate, desc_yourself, desc_you, sex):
    try:
        conn = sqlite3.connect("mate.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM mate WHERE id = ?", (id,))
        count = cur.fetchone()
        print(count)

        if count:
            sql = "UPDATE mate SET name = ?, address = ?, age = ?, price = ?, sex_mate = ?, desc_yourself = ?, desc_you = ?, sex = ?, is_on = ? WHERE id = ?"
            cur.execute(sql, (name, address, age, price, sex_mate, desc_yourself, desc_you, sex, 1, id))
        else:
            sql = "INSERT INTO mate (id, name, username, address, age, price, sex_mate, desc_yourself, desc_you, sex, is_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur.execute(sql, (id, name, username, address, age, price, sex_mate, desc_yourself, desc_you, sex, 1))

        conn.commit()

        print("[DEBUG] Данные добавлены, новый пользователь в таблице mate")
        print(
            f"{id=}, {name=}, {username=}, {address=}, {age=}, {price=}, {sex_mate=}, {desc_yourself=}, {desc_you=}, {sex=}")
        print()


    except Exception as e:
        print(e)


def del_mate(id, is_on):
    try:
        conn = sqlite3.connect("mate.db")
        cur = conn.cursor()

        cur.execute("UPDATE mate SET is_on = ? WHERE id = ?", (is_on, id,))

        conn.commit()

        print(f"[DEBUG] запись удалена {id=}")

    except Exception as e:
        print(e)


def feed_mate(id, address, sex_mate, sex):
    try:
        conn = sqlite3.connect("mate.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM mate WHERE id != ? AND address = ? AND sex = ? AND sex_mate = ?",
                    (id, address, sex_mate, sex))
        count = cur.fetchall()

        conn.commit()

        print("[DEBUG] Данные получены из таблицы mate")
        print()

        return count

    except Exception as e:
        print(e)

#####################################################################
"""STUDLIFE SKILLS"""

def get_id_skills():
    try:
        conn = sqlite3.connect("skills.db")
        cur = conn.cursor()

        cur.execute("SELECT id FROM skills")
        count = cur.fetchall()

        conn.commit()

        print("[DEBUG] Данные id получены")
        print()

        return count

    except Exception as e:
        print(e)


def get_skills(id):
    try:
        conn = sqlite3.connect("skills.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM skills WHERE id = ?", (id,))
        count = cur.fetchone()
        print(count)

        conn.commit()

        print("[DEBUG] Данные полученны из mate")
        print(count)
        print()

        if count:
            return count
        else:
            return [None] * 9

    except Exception as e:
        print(e)


def register_skills(id, name, username, address, age, sex_mate, desc_yourself, desc_you, sex):
    try:
        conn = sqlite3.connect("skills.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM skills WHERE id = ?", (id,))
        count = cur.fetchone()
        print(count)

        if count:
            sql = "UPDATE skills SET name = ?, address = ?, age = ?, sex_mate = ?, desc_yourself = ?, desc_you = ?, sex = ?, is_on = ? WHERE id = ?"
            cur.execute(sql, (name, address, age, sex_mate, desc_yourself, desc_you, sex, 1, id))
        else:
            sql = "INSERT INTO skills (id, name, username, address, age, sex_mate, desc_yourself, desc_you, sex, is_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur.execute(sql, (id, name, username, address, age, sex_mate, desc_yourself, desc_you, sex, 1))

        conn.commit()

        print("[DEBUG] Данные добавлены, новый пользователь в таблице skills")
        print(
            f"{id=}, {name=}, {username=}, {address=}, {age=}, {sex_mate=}, {desc_yourself=}, {desc_you=}, {sex=}")
        print()


    except Exception as e:
        print(e)


def del_skills(id, is_on):
    try:
        conn = sqlite3.connect("skills.db")
        cur = conn.cursor()

        cur.execute("UPDATE skills SET is_on = ? WHERE id = ?", (is_on, id,))

        conn.commit()

        print(f"[DEBUG] запись удалена {id=}")

    except Exception as e:
        print(e)


def feed_skills(id, address, sex_mate, sex):
    try:
        conn = sqlite3.connect("skills.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM skills WHERE id != ? AND address = ? AND sex = ? AND sex_mate = ?",
                    (id, address, sex_mate, sex))
        count = cur.fetchall()

        conn.commit()

        print("[DEBUG] Данные получены из таблицы skills")
        print()

        return count

    except Exception as e:
        print(e)