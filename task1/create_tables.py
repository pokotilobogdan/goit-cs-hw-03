import psycopg2


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print(e)


if __name__ == '__main__': 

    # Database connection parameters
    hostname = 'localhost'
    database = 'postgres'
    username = 'postgres'
    password = 'mysecretpassword'
    port = 5432  # Default port for PostgreSQL

    try:
        # Establish the connection
        with psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=password,
            port=port
        ) as conn:
            
            # Create a cursor object
            with conn.cursor() as cur:
                sql_create_users_table = '''CREATE TABLE users (
                                                id SERIAL PRIMARY KEY,
                                                fullname VARCHAR(100),
                                                email VARCHAR(100) UNIQUE
                                            );'''

                sql_create_status_table = '''CREATE TABLE status (
                                                id SERIAL PRIMARY KEY,
                                                name VARCHAR(50) UNIQUE
                                            );'''

                sql_create_tasks_table = '''CREATE TABLE tasks (
                                                id SERIAL PRIMARY KEY,
                                                title VARCHAR(100),
                                                description TEXT,
                                                status_id INT,
                                                user_id INT,
                                                FOREIGN KEY (status_id) REFERENCES status (id)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
                                                FOREIGN KEY (user_id) REFERENCES users (id)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                                            );'''

                create_table(conn, sql_create_users_table)
                create_table(conn, sql_create_status_table)
                create_table(conn, sql_create_tasks_table)

    except Exception as e:
        print(f"Error: {e}")