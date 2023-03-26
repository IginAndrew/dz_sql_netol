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
            cur.execute(
                """
                SELECT phone.phone from phone 
                WHERE phone = %s; 
                """,
                (phone,)  # Передаем номер телефона
            )
            if cur.fetchone():
                return print("такой номер есть, добавление номера невозможно")  # Соообщаем что такой номер есть
            conn.rollback()
            cur.execute("""
                    INSERT INTO phone(phone, client_id) VALUES(%s, %s) RETURNING id
                    """, (phone, client[0],))
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
            (phone, client_id,)
        )
        conn.commit()  # Подтверждаем изменения
        return print("успех")  # Возвращаем сообщение об успехе


def change_client_2(conn, id, first_name=None, last_name=None, e_mail=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, last_name, e_mail, id FROM client WHERE id = %s
        """, (id, ))
        id_clienta = cur.fetchone()
        if not id_clienta:
            return print('такого клиента нет')
        id_clienta_list = list(id_clienta)
        print(id_clienta_list)
        if first_name is not None:
            id_clienta_list[0] = first_name
        else:
            first_name = id_clienta_list[0]
        if last_name is not None:
            id_clienta_list[1] = last_name
        else:
            last_name = id_clienta_list[1]
        if e_mail is not None:
            id_clienta_list[2] = e_mail
        else:
            e_mail = id_clienta_list[2]
        cur.execute("""
        UPDATE client SET first_name=%s, last_name=%s, e_mail=%s WHERE id=%s
        """, (first_name, last_name, e_mail, id,))
        conn.commit()
    return "Пользователь успешно изменен"

def delete_phone(conn, id: str):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phone WHERE id=%s;
            """, (id,))


def delete_client(conn, id: str):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM client WHERE id=%s;
                """, (id,))



def find_client_1(conn, first_name=None, last_name=None, e_mail=None, phone=None):
    with conn.cursor() as cur:
        if first_name is None: # Если имя не было передано
            first_name = '%'  # Определяем новое значение, которое означает, что здесь может быть любая строка
        if last_name is None:  # Если фамилия не была передана
            last_name = '%'  # Определяем новое значение, которое означает, что здесь может быть любая строка
        if e_mail is None:  # Если почта не была передана
            e_mail = '%'  # Определяем новое значение, которое означает, что здесь может быть любая строка
        list_client = [first_name, last_name, e_mail, ]  # Создаем список из имени, фамилии и почты
        new_str = ''  #Определяем переменную с пустой строкой. Далее эта строка будет вставляться в тело запоса.
        if phone is not None:  #Если телефон содержит значение
            new_str = 'AND ARRAY_AGG(phone.phone) && ARRAY[%s]'  #Присваиваем переменной, которую определили через строку выше, новое значение с условием поиска телефона (в данном условии происходит пересечение массивов). Вместо точек указываем столбец с номерами из таблицы номеров.
            list_client.append(phone)  #Добавляем в ранее созданный список телефон, который передали в функцию.
        select_client = f"""
        SELECT  e_mail, first_name,last_name, CASE
                WHEN ARRAY_AGG (phone.phone) = '{{Null}}' THEN ARRAY[]::BIGINT[]
                ELSE ARRAY_AGG (phone.phone)
            END phone
        FROM client
        LEFT JOIN phone ON client.id = phone.client_id
        GROUP BY client.e_mail, client.first_name, client.last_name
        HAVING client.e_mail LIKE %s AND client.first_name LIKE %s AND client.last_name LIKE %s {new_str}
        """
        cur.execute(
            select_client,  #Передаем переменную с запросом
            (list_client) #Передаем список с значениями, который создали ранее
        )
        return print(*cur.fetchall())

with psycopg2.connect(database="py_sql", user="andrew", password="12048937") as conn:
    # create_client_phone(conn)
    # add_client(conn, "Pety", "Valadimirov", "ladimirov@ya.ru", 85858742156)
    # change_client_2(conn, id=10, first_name='Jupkin')
    # delete_phone(conn, '1')
    # delete_client(conn, '3')
    find_client_1(conn, last_name='Dima')
    # add_phone_2(conn, 89513875023, 8)
