import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        DROP TABLE phone;
        DROP TABLE clients;
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id),
        number VARCHAR(30)
        );
        ''')
        conn.commit()

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id, first_name, last_name, email;
        ''', (first_name, last_name, email))
        print(cur.fetchone())

def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO phone(client_id, number) VALUES(%s, %s) RETURNING id, client_id, number;
        ''', (client_id, number))
        print(cur.fetchone())

def change_email(conn, email, id):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE clients SET email=%s WHERE id=%s;
        ''', (email, id))
        cur.execute('''
        SELECT * FROM clients;
        ''')
        print(cur.fetchall())

def delete_phone(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM phone WHERE client_id=%s;
        ''', (client_id,))
        cur.execute('''
                SELECT * FROM phone;
                ''')
        print(cur.fetchall())

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients WHERE id=%s;
        ''', (client_id,))
        cur.execute('''
                SELECT * FROM clients;
                ''')
        print(cur.fetchall())

def find_client(conn, first_name=None, last_name=None, email=None, number=None):
    if first_name:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT * FROM clients WHERE first_name = %s;
            ''', (first_name,))
            print(f'В базе данных есть клиенты с именем {first_name}: ', cursor.fetchall())

    if last_name:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT * FROM clients WHERE last_name = %s;
            ''', (last_name,))
            print(f'В базе данных есть клиенты с фамилией {last_name}: ', cursor.fetchall())

    if email:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT * FROM clients WHERE email=%s;
            ''',(email,))
            print(f'В базе данных есть клиенты с email {email}: ', cursor.fetchall())

    if number:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT * FROM clients c
            JOIN phone p ON c.id = p.client_id WHERE p.number=%s;
            ''', (number,))
            print(f'В базе данных есть клиенты с номером {number}: ', cursor.fetchall())

with psycopg2.connect(database='clients_db', user='postgres') as conn:
    create_db(conn)
    add_client(conn, 'Anton', 'Borisov', 'borisov2011@gmail.com')
    add_client(conn, 'Anton', 'Ivanov', 'ivanov2011@mail.ru')
    add_client(conn, 'Andrey', 'Borisov', 'borisoff@gmail.com')
    add_phone(conn, 1, '89214201776')
    add_phone(conn, 1, '89959001776')
    change_email(conn, 'borisov2011@icloud.com', 1)
    # delete_phone(conn, 1)
    # delete_client(conn, 1)
    find_client(conn, first_name='Anton')
    find_client(conn, last_name='Borisov')
    find_client(conn, email='borisov2011@icloud.com')
    find_client(conn, number='89959001776')

conn.close()
