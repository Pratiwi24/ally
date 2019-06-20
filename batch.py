import sqlite3
from sqlite3 import Error

def create_connection():
    try:
        conn = sqlite3.connect('toba.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM catalog")
        print(conn)
    except Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    create_connection()
