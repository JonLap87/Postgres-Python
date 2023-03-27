import psycopg2

conn = psycopg2.connect(database="netology_db", user="postgres", password="220261")
def create_db(conn):
    with conn.cursor() as cur:
    # удаление таблиц
        cur.execute("""
        DROP TABLE telefon;
        DROP TABLE client;
        """)

        # создание таблиц
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) UNIQUE,
            lastname VARCHAR(40) UNIQUE,
            email VARCHAR(80) UNIQUE
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telefon(
            id SERIAL PRIMARY KEY,
            number BIGINT NOT NULL,
            client_id INTEGER NOT NULL REFERENCES client(id)
            );
            """)
        conn.commit()  # фиксируем в БД

def add_client(conn, name, lastname, email, number=None):
    with conn.cursor() as cur:
        # наполнение таблиц (telefon,client)
        cur.execute("""
            INSERT INTO client(name,lastname,email) VALUES
            ('Tom', 'Adoms', 'adom@mail.ru') RETURNING id;
            """)
        print(cur.fetchone())  # запрос данных автоматически зафиксирует изменения
        cur.execute("""
            INSERT INTO client(name,lastname,email) VALUES
            ('Jon', 'Varon', 'samual@mail.com') RETURNING id;
            """)
        print(cur.fetchone())  # запрос данных автоматически зафиксирует изменения

def add_telefon (conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO telefon(number, client_id) VALUES
            (9109452204, 1) RETURNING id, number;
            """)
        cur.execute("""
            INSERT INTO telefon(number, client_id) VALUES
            (9101702023, 2) RETURNING id, number;
            """)
        print(cur.fetchone())  # запрос данных автоматически зафиксирует изменения 

def change_client(conn, client_id, name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        # обновление данных (client)
        cur.execute("""
            UPDATE client SET name=%s, lastname=%s,email=%s WHERE name=%s;
            """, ('Kal', 'Rot', 'rot@mail.com', 'Tom'))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

def delete_telefon(conn, client_id, number):
    with conn.cursor() as cur:
        # удаление данных (удаляем телефон сущ клиента)
        cur.execute("""
            DELETE FROM telefon WHERE client_id=%s;
            """, (1,))
        cur.execute("""
            SELECT * FROM telefon;
            """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

def delete_client(conn, name):
    with conn.cursor() as cur:
        # удаление данных (сущ клиента)
        cur.execute("""
            DELETE FROM client WHERE name=%s;
            """, ('Kal',))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

def find_client(conn, name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        # выборка данных
        cur.execute("""
            SELECT id FROM client WHERE name=%s;
            """, ('Jon',))  # хорошо, обратите внимание на кортеж
        print(cur.fetchone())
conn.close()