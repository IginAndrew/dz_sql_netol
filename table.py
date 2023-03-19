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


def add_client(conn, id, first_name=None, last_name=None, e_mail=None):

    with conn.cursor() as cur:
        cur.execute(f"""
                   INSERT INTO client VALUES ('{id}', '{first_name}', '{last_name}', '{e_mail}');
               """)


# def add_phone(conn, id, phone, client_id):
#
#     with conn.cursor() as cur:
#         cur.execute(f"""
#                    INSERT INTO phone VALUES ('{id}', '{phone}', '{client_id}');
#                """)


def add_phone_2(conn, id: int, phone: int, client_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT phone.phone from phone 
            WHERE phone = %s; 
            """,
            (phone,)  # Передаем номер телефона
        )
        if cur.fetchone():  # Проверяем вернулась ли не пустая коллекция
            print(cur.fetchone())
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
            INSERT INTO phone(id, phone, client_id) VALUES ( 
                %s, %s, %s
            );
            """,
            (id, phone, client_id)
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
        cur.execute("""
            SELECT first_name, last_name, e_mail FROM client
            JOIN phone ON phone.client_id = client.id
            WHERE first_name=%s OR last_name=%s OR e_mail=%s OR phone=%s;
            """, (first_name, last_name, e_mail, phone))
        print(*cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="py_sql", user="andrew", password="12048937") as conn:
        with conn.cursor() as cur:
            # create_db(conn, cur)
            # create_client_phone(conn)
            # add_client(conn, 3, "ANDREY", "FIGIN", "andefig@ya.ru")
            # add_phone(conn, 1, 89513284054, 1)
            # change_client(conn, 1, 'Andrew')
            # delete_phone(conn, '1')
            # delete_client(conn, '3')
            find_client(conn, None, None, None, 89513284055)
            # add_phone_2(conn, 9, 89513274016, 2)
