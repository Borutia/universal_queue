import psycopg2

from sql import SQL_TABLES
from tools.const import CONNECTION_STRING


def main():
    with psycopg2.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(SQL_TABLES)


if __name__ == '__main__':
    main()
