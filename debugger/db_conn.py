import psycopg2

from config import db_endpoint, db_name, db_key


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(
            host=db_endpoint,
            port='5432',
            database=db_name,
            user=db_name,
            password=db_key,
        )

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), '\n')

        # Print PostgreSQL version
        cursor.execute('SELECT version();')
        record = cursor.fetchone()
        print('You are connected to - ', record, '\n')

    except (Exception, psycopg2.Error) as error:
        print('Error while connecting to PostgreSQL', error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')
