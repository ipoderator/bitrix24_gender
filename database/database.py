import psycopg2

from create_gender import get_gender
from parsing_name import list_names


def create_base(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS gender(
        id INTEGER PRIMARY KEY,
        name VARCHAR(10));
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY UNIQUE,
        name VARCHAR(50) NOT NULL,
        gender_id INTEGER REFERENCES gender(id))
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS names_woman(
        id INTEGER PRIMARY KEY,
        name VARCHAR(50));
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS names_man(
        id INTEGER PRIMARY KEY,
        name VARCHAR(50));
        """)


def get_data(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT FROM gender;
        SELECT FROM names_woman;
        SELECT FROM names_man
        """)
        return cur.fetchone()


def add_gender(conn, names_gender):
    for i, j in enumerate(names_gender):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO gender(id, name) VALUES (%s,%s);
            """, (i+1, j))


def add_names_woman(conn, names):
    for i, j in enumerate(names):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO
            names_woman(id, name) VALUES (%s,%s);
            """, (i+1, j))


def add_names_man(conn, names):
    for i, j in enumerate(names):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO
            names_man(id, name) VALUES (%s, %s);
            """, (i+1, j))


def get_id_name_woman(conn, name):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id FROM names_woman WHERE name = %s;
        """, (name, ))
        return cur.fetchall()


def get_id_name_man(conn, name):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id FROM names_man WHERE name = %s;
        """, (name, ))
        return cur.fetchone()


def get_data_contact(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT c.id,g.name FROM contacts c
        JOIN gender g ON c.gender_id=g.id
        WHERE c.id = %s;
        """, (id, ))
        return cur.fetchall()


def contacts_upload(conn, data, id):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO contacts(id, name, gender_id)
        VALUES(%s, %s, %s);
        """, (data['ID'], data['NAME'], id))


def update_contact_gender(bx, data_db,  database, user, password):
    with psycopg2.connect(
        database=database, user=user, password=password
            ) as conn:
        create_base(conn)
        names_gender = ['Мужчина', 'Женщина']
        add_gender(conn, names_gender)
        add_names_woman(conn, list_names('female'))
        add_names_man(conn, list_names('male'))
        for data in data_db:
            if len(get_id_name_woman(conn, data['NAME'])) != 0:
                contacts_upload(conn, data, 2)
                dat = get_data_contact(conn, data['ID'])
                get_gender(bx, data['ID'], dat[0][1])
            else:
                contacts_upload(conn, data, 1)
                dat = get_data_contact(conn, data['ID'])
                get_gender(bx, data['ID'], dat[0][1])
