import pytest
import psycopg2
from pgcli.main import format_output

# TODO: should this be somehow be divined from environment?
POSTGRES_USER, POSTGRES_HOST = 'postgres', 'localhost'


def db_connection(dbname=None):
    conn = psycopg2.connect(user=POSTGRES_USER, host=POSTGRES_HOST, dbname=dbname)
    conn.autocommit = True
    return conn

try:
    db_connection()
    CAN_CONNECT_TO_DB = True
except:
    CAN_CONNECT_TO_DB = False

dbtest = pytest.mark.skipif(
    not CAN_CONNECT_TO_DB,
    reason="Need a postgres instance at localhost accessible by user 'postgres'")


def create_db(dbname):
    with db_connection().cursor() as cur:
        try:
            cur.execute('''CREATE DATABASE _test_db''')
        except:
            pass


def drop_tables(conn):
    with conn.cursor() as cur:
        cur.execute('''DROP SCHEMA public CASCADE; CREATE SCHEMA public''')


def run(executor, sql, join=False):
    " Return string output for the sql to be run "
    result = []
    for rows, headers, status in executor.run(sql):
        result.extend(format_output(rows, headers, status))
    if join:
        result = '\n'.join(result)
    return result
