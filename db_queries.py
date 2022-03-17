from settings import username, password
from mysql.connector import connect
import random


def connect_to_mysql_db():
    connection = connect(
        host='localhost',
        user=username,
        password=password,
        database='films'
    )
    return connection


# TODO Замінити чистий SQL на sql alchemy
def add_value_to_db(user_info: str, name_of_table: str):
    with connect_to_mysql_db() as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO {name_of_table} (title)
        VALUES (%s)
        """, (user_info,))
        connection.commit()


def read_films_from_db(content: str):
    with connect_to_mysql_db() as connection:
        select_movies_query = f"SELECT title FROM {content}"
        cursor = connection.cursor()
        cursor.execute(select_movies_query)
        result = cursor.fetchall()
        if not result:
            random_value = 'Список пустий'
            return random_value
        random_value = random.choice(result)
        value_for_deleting = random_value[0]
        cursor.execute(f"""DELETE FROM {content} WHERE title = (%s)""", (value_for_deleting,))
        connection.commit()
    return random_value
