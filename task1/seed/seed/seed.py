import faker
from random import randint, random
import psycopg2


NUMBER_TASKS = 10
NUMBER_USERS = 10


fake_data = faker.Faker()

def generate_email(name):
    username = name.lower().replace(' ', '.')
    domain = fake_data.free_email_domain()
    return f"{username}@{domain}"


def generate_fake_data(number_users, number_tasks) -> tuple():
    fake_users = []                 # тут зберігатимемо співробітників
    fake_task_titles = []           # тут зберігатимемо назви завдань
    fake_task_descriptions = []     # тут зберігатимемо описи завдань

# Згенеруємо тепер number_users кількість користувачів
    for _ in range(number_users):
        fake_users.append(fake_data.name())
        
# Згенерованим користувачам надамо електроні пошти
    fake_emails = [generate_email(user) for user in fake_users]

# Створимо назви завдань рандомними англійськими реченнями
    for _ in range(number_tasks):
        fake_task_titles.append(fake_data.sentence())

# Доповнимо завдання рандомними англійськими абзацами З МОЖЛИВІСТЮ ЗАВДАНЬ БЕЗ ОПИСУ
    for _ in range(number_tasks):
        if random() > 0.25:
            fake_task_descriptions.append(fake_data.paragraph())
        else:
            fake_task_descriptions.append('')

    return fake_users, fake_emails, fake_task_titles, fake_task_descriptions


def prepare_data(users, emails, task_titles, task_descriptions) -> tuple():

    for_status = [('new',), ('in process',), ('completed',)]         # для таблиці status

    for_users = []                                          # для таблиці users
    for user, email in zip(users, emails):
        for_users.append((user, email))
        
    for_tasks = []                                          # для таблиці tasks
    for task_title, task_description in zip(task_titles, task_descriptions):
        for_tasks.append((task_title, task_description, randint(1, NUMBER_USERS), randint(1, len(for_status))))

    return for_status, for_users, for_tasks


def insert_data(hostname, database, username, password, port, data):
    """
    Inserts data into a PostgreSQL table.

    Args:
    hostname (str): The database host.
    database (str): The name of the database.
    username (str): The database user.
    password (str): The user's password.
    port (int): The port number to connect to.
    table (str): The name of the table where data will be inserted.
    data (tuple): The data to be inserted into the table.
    
    data = (status, users, tasks)
    """
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
                
                status, users, tasks = data[0], data[1], data[2]

        # Скрипт для того, щоб при перезапуску програми індекси статусів були в межах від 1 до 3
                sql_preserve_status = """
                TRUNCATE TABLE status CASCADE;
                ALTER SEQUENCE status_id_seq RESTART WITH 1;
                """
                cur.execute(sql_preserve_status)

                sql_to_status = """INSERT INTO status (name) VALUES (%s)"""

                cur.executemany(sql_to_status, status)          


        # Скрипт для того, щоб при перезапуску програми індекси користувачів були в межах від 1 до 10
                sql_preserve_users = """
                TRUNCATE TABLE users CASCADE;
                ALTER SEQUENCE users_id_seq RESTART WITH 1;
                """
                cur.execute(sql_preserve_users)

        # Далі вставляємо дані про користувачів
                sql_to_users = """INSERT INTO users (fullname, email) VALUES (%s, %s)"""

        # Дані були підготовлені заздалегідь, тому просто передаємо їх у функцію
                cur.executemany(sql_to_users, users)
                conn.commit()           # На цьому етапі треба зберегти дані, бо інакше ми не зможемо заповнити таблицю tasks, бо не буде чим


        # Скрипт для того, щоб при перезапуску програми індекси задач були в межах від 1 до 69
                sql_preserve_tasks = """
                TRUNCATE TABLE tasks CASCADE;
                ALTER SEQUENCE tasks_id_seq RESTART WITH 1;
                """
                cur.execute(sql_preserve_tasks)
                
        # Заповнюємо базу даних задачами
                sql_to_tasks = """INSERT INTO tasks (title, description, user_id, status_id)
                                      VALUES (%s, %s, %s, %s)"""

                cur.executemany(sql_to_tasks, tasks)
                conn.commit()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    
    # Database connection parameters
    hostname = 'localhost'
    database = 'postgres'
    username = 'postgres'
    password = 'mysecretpassword'
    port = 5432  # Default port for PostgreSQL

    container_connect_data = hostname, database, username, password, port

    status, users, tasks = prepare_data(*generate_fake_data(NUMBER_USERS, NUMBER_TASKS))
    
    # print(users)
    # print(tasks)

    insert_data(*container_connect_data, (status, users, tasks))
