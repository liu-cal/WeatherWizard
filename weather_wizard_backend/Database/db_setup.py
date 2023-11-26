import sqlite3
from sqlite3 import Error


def get_connection():
    return sqlite3.connect('weather.db')


def create_connection():
    connection = get_connection()

    try:
        with open('schema.sql') as f:
            connection.executescript(f.read())
        connection.commit()
        connection.close()
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()