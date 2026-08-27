import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="spam_detection",
        user="postgres",
        password="PostgreSQL"
    )

    return connection