import psycopg2

# создаём базу данных

def create_db():
	connect = psycopg2.connect(user="postgres", password="")
	with connect.cursor() as cur:
		connect.autocommit = True
		cur.execute("CREATE DATABASE homework")
		connect.commit()  # фиксируем в БД

# 1 Функция, создающая структуру БД (таблицы).
def create_table(connect):
    with connect.cursor() as cur:
        cur.execute("""
			CREATE TABLE IF NOT EXISTS client(
			client_id SERIAL PRIMARY KEY,
			name VARCHAR(40) NOT NULL,
			surname VARCHAR(40) NOT NULL
			);
        """)

        connect.commit()  # фиксируем в БД

        cur.execute("""
		 	CREATE TABLE IF NOT EXISTS phone_book(
		    phone_id SERIAL PRIMARY KEY,
		    client_id INTEGER REFERENCES client(client_id),
			phone CHAR(12),
			email VARCHAR(40)
		    );
        """)
        connect.commit()  # фиксируем в БД


# 2 Функция, позволяющая добавить нового клиента.
def add(conn, name, surname, email, phones=None):
    with conn.cursor() as cur:
        cur.execute(f"""
		 	INSERT INTO client( name, surname, email) values ('{name}', '{surname}', '{email}');
			 	""")
        conn.commit()


# 3 Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(f"""
		    INSERT INTO phone_book(client_id, phone) VALUES('{client_id}', '{phone}');
		    """)
        conn.commit()


# 4 Функция, позволяющая изменить данные о клиенте.

def change_client(conn, client_id, name=None, surname=None, email=None, phones=None, phone_id=None):
    with conn.cursor() as cur:
        cur.execute(f'''
			UPDATE phone_book
			SET phone = '{phones}'
			WHERE phone_id = '{phone_id}';
			UPDATE client
			SET name = '{name}', surname = '{surname}', email = '{email}'
			WHERE client_id = '{client_id}';
			''')
        conn.commit()


# 5 Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(f'''
			DELETE FROM phone_book
			WHERE phone = '{phone}' and client_id = '{client_id}';
			''')
        conn.commit()


# 6 Функция, позволяющая удалить существующего клиента.

def delete(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
			delete from client 
			where client_id = 2;
			
			delete from phone_book 
			where client_id = 1;
			''')
        conn.commit()


# 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(conn, name=None, surname=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute(f'''
			select '{name}', '{surname}', '{email}', '{phone}' from client 
			full outer join
			phone_book on client.client_id = phone_book.client_id;
			''')
        res = cur.fetchall()
        return res

# создаём таблицы
with psycopg2.connect(database='homework', user='postgres', password='') as connect:
    create_db(connect)
    create_table(connect)
    name = input('Введите имя: ')
    surname = input('Введите отчество: ')
    email = input('Введите email: ')
    client_id = input('Введите client_id: ')
    phones = input('Введите phones: ')
    phone_id = input('Введите phone_id: ')
    phone = input('Введите phone: ')
    add(connect, name, surname, email)
    add_phone(connect, client_id, phone)
    change_client(connect, client_id, name, surname, email, phones, phone_id)
    delete_phone(connect, client_id, phone )
    find_client(connect, name, surname, email, phone)
    question = input('Введите один из параметров клиента: ')
    response = find_client(connect)
    for el in response:
        if question in el:
            print(el)

connect.close()