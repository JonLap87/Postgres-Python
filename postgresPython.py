import psycopg2

conn = psycopg2.connect(database="netology_db", user="postgres", password="220261")
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

        # наполнение таблиц (telefon,client)
        cur.execute("""
            INSERT INTO client(name,lastname,email) VALUES
            ('Tom', 'Adoms', 'adom@mail.ru') RETURNING id;
            """)
        cur.execute("""
             INSERT INTO client(name,lastname,email) VALUES
            ('Jon', 'Varon', 'samual@mail.com') RETURNING id;
            """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

        cur.execute("""
            INSERT INTO telefon(number, client_id) VALUES
            (9109452204, 1) RETURNING id, number;
            """)
        cur.execute("""
            INSERT INTO telefon(number, client_id) VALUES
            (9101702023, 2) RETURNING id, number;
            """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения 

        # обновление данных (client)
        cur.execute("""
            UPDATE client SET name=%s, lastname=%s,email=%s WHERE name=%s;
            """, ('Kal', 'Rot', 'rot@mail.com', 'Tom'))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

        # удаление данных (удаляем телефон сущ клиента)
        def get_del_telefon(cursor, name: str) -> int:
            cursor.execute("""
            DELETE FROM telefon WHERE client_id=%s;
            """, (1,))
            cursor.execute("""
            SELECT * FROM telefon;
            """)
            return cur.fetchone()[1]
        telefon = get_del_telefon(cur, 1)
        print('telefon', telefon)

        # удаление данных (сущ клиента)
        def get_del_client(cursor, name: str) -> int:
            cursor.execute("""
            DELETE FROM client WHERE name=%s;
            """, ('Kal',))
            cursor.execute("""
            SELECT * FROM client;
            """)
            return cur.fetchone()[1]
        name = get_del_client(cur, 'Jon')
        print('client', name)
    
        # выборка данных
        def get_course_id(cursor, name: str) -> int:
            cursor.execute("""
            SELECT id FROM client WHERE name=%s;
            """, (name,))
            return cur.fetchone()[0]
        id = get_course_id(cur, 'Jon')
        print('jon_id', id)


conn.close()