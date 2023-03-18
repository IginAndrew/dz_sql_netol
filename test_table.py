import psycopg2

def create_db():
    cur = conn.cursor()
    return cur

def add_client():
    create_db()
    with conn.cursor() as cur:
        cur.execute("""
        create table if not exists client (
    	id INTEGER PRIMARY KEY,
    	first_name varchar(40) not null,
    	last_name  varchar(40) not null,
    	email  varchar(40) not null UNIQUE 
        );
        """)
    return cur.execute

def add_phone():
    create_db()
    with conn.cursor() as cur:
        cur.execute("""
            create table if not exists phone (
        	id INTEGER PRIMARY KEY,
        	phone integer not null,
        	client_id INTEGER NOT NULL REFERENCES client(id)
        	);
        """)
    return cur.execute

def change_client(id: int, first_name: str, last_name: str, email: str):
    create_db()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client (id, first_name, last_name, email) VALUES(%s, %s, %s, %s
            );
        """, (id, first_name, last_name, email))
    return cur.execute

def add_phone_in(id:int, phone:int, client_id:int ):
    create_db()
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone (id, phone, client_id) VALUES(%s, %s, %s
            );
        """, (id, phone, client_id))
    return cur.execute

def change_client_up(id, first_name: str):
    create_db()
    with conn.cursor() as cur:
        cur.execute("""UPDATE client SET first_name = %s where id = %s;
        """, (first_name, id))
        print(cur.rowcount)
    return cur.execute

def delete_phone(id: str):
    create_db()
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phone WHERE id=%s;
            """, (id))
        print(cur.rowcount)
    return cur.execute

def delete_client(id: str):
    create_db()
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM client WHERE id=%s;
                """, (id))
        print(cur.rowcount)
    return cur.execute

def find_client(zapros):
    create_db()
    with conn.cursor() as cur:
        cur.execute(zapros)
        for person in cur.fetchall():
            print(*person)



with psycopg2.connect(database="postgres", user="andrew", password="12048937") as conn:
    # change_client(4, "Andrew", "Figin", "andrewigin@ya.ru")
    # add_phone_in(4, 895132, 1)
    # change_client_up(1, "Andrew")
    # delete_phone("1")
    # delete_client("2")
    # find_client("""SELECT client.first_name, client.last_name, phone.phone
    # FROM client JOIN phone ON  client.id = phone.client_id and phone = 325
    #     """)
    conn.commit()

conn.close()