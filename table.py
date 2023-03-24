import psycopg2


def create_client_phone(conn):
    with conn.cursor() as cur:
        cur.execute("""
        create table if not exists client
        (
        id SERIAL PRIMARY KEY,
        first_name varchar(40) not null,
        last_name  varchar(40) not null,
        e_mail  varchar(40) not null UNIQUE
        );
        """)
        cur.execute("""
                create table if not exists phone (
            	id SERIAL PRIMARY KEY,
            	phone integer not null UNIQUE,
            	client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE
            	);
            """)


def add_client(conn, first_name=None, last_name=None, e_mail=None, phone=None):

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT client.e_mail from client 
            WHERE client.e_mail = %s; 
            """,
            (e_mail,)  # Передаем email
        )
        if cur.fetchone():  # Проверяем вернулась ли не пустая коллекция
            return print("такой email есть")  # Соообщаем что такой emal есть

        cur.execute(f"""
                   INSERT INTO client (first_name, last_name, e_mail) VALUES ('{first_name}', '{last_name}', '{e_mail}') RETURNING id;
               """)
        client = cur.fetchone()
        if phone is not None:
            cur.execute("""
                    INSERT INTO phone(phone, client_id) VALUES(%s, %s) RETURNING id
                    """, (phone, client[0]))
            client_phone = cur.fetchone()
            if client_phone == "такой номер есть":
                conn.rollback()
                return print("добавление невозможно")
            conn.commit()
    print(f'Добавили клиента {client}')


def add_phone_2(conn, phone: int, client_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT phone.phone from phone 
            WHERE phone = %s; 
            """,
            (phone,)  # Передаем номер телефона
        )
        if cur.fetchone():  # Проверяем вернулась ли не пустая коллекция
            return print("такой номер есть")  # Соообщаем что такой номер есть
        cur.execute(
            """
            SELECT client_id from phone
            WHERE client_id = %s; 
            """,
            (client_id,)  # Передаем id клиента
        )
        if not cur.fetchone():  # Проверяем вернулась ли пустая коллекция
            return print("такого клиента нет")  # Соообщаем что такого клиента нет
        cur.execute(
            """
            INSERT INTO phone(phone, client_id) VALUES ( 
            %s, %s
            ) RETURNING id;
            """,
            (phone, client_id)
        )
        conn.commit()  # Подтверждаем изменения
        return print("успех")  # Возвращаем сообщение об успехе


def change_client(conn, id, first_name=None, last_name=None, e_mail=None):
    with conn.cursor() as cur:
        cur.execute(f"""
                       UPDATE client SET first_name = '{first_name}'
                       WHERE id = '{id}';
                   """)


def delete_phone(conn, id: str):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phone WHERE id=%s;
            """, (id,))


def delete_client(conn, id: str):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM client WHERE id=%s;
                """, (id,))


def find_client(conn, first_name=None, last_name=None, e_mail=None, phone: int = None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT first_name, last_name, e_mail FROM client
            JOIN phone ON phone.client_id = client.id
            WHERE first_name=%s OR last_name=%s OR e_mail=%s OR phone=%s;
            """, (first_name, last_name, e_mail, phone))
        print(*cur.fetchall())

with psycopg2.connect(database="py_sql", user="andrew", password="12048937") as conn:
    # create_client_phone(conn)
    # add_client(conn, "Pety", "Vai", "vai@ya.ru", 85858742156)
    # change_client(conn, 1, 'Andrew')
    # delete_phone(conn, '1')
    # delete_client(conn, '3')
    find_client(conn, None, None, None, 89522365478)
    # add_phone_2(conn, 89513875023, 8)
