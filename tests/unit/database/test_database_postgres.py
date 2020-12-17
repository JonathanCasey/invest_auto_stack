#!/usr/bin/env python3
"""
Tests the grand_trade_auto.general.database_postgres functionality.

Per [pytest](https://docs.pytest.org/en/reorganize-docs/new-docs/user/naming_conventions.html),
all tiles, classes, and methods will be prefaced with `test_/Test` to comply
with auto-discovery (others may exist, but will not be part of test suite
directly).

Module Attributes:
  N/A

(C) Copyright 2020 Jonathan Casey.  All Rights Reserved Worldwide.
"""
import psycopg2
import pytest

from grand_trade_auto.database import database_postgres
from grand_trade_auto.database import databases



@pytest.fixture(name='pg_test_db')
def fixture_pg_test_db():
    """
    Gets the test database handle for postgres.

    Returns:
      (DatabasePostgres): The test postgres database handle.
    """
    return databases.get_database_from_config('test', 'postgres')



def test_load_from_config(pg_test_db):
    """
    Tests the `load_from_config()` method in `DatabasePostgres`.

    TODO: This should load its own conf files and test directly; but good enough
    for now.
    """
    assert pg_test_db is not None



def test_get_type_names():
    """
    Tests the `get_type_names()` method in `DatabasePostgres`.  Not an
    exhaustive test.
    """
    assert 'postgres' in database_postgres.DatabasePostgres.get_type_names()
    assert 'not-postgres' not in \
            database_postgres.DatabasePostgres.get_type_names()



def test_connect(pg_test_db):
    """
    Tests the `connect()` method in `DatabasePostgres`.  Only tests connecting
    to the default database; connecting to the real test db will be covered by
    another test.
    """
    conn = pg_test_db.connect(cache=False, database='postgres')
    assert conn is not None

    pg_test_db.database = 'invalid-database'
    with pytest.raises(psycopg2.OperationalError):
        conn = pg_test_db.connect()

    pg_test_db.conn = 'test-conn'
    assert pg_test_db.connect() == 'test-conn'
    assert pg_test_db.conn == 'test-conn'



def test_check_if_db_exists(pg_test_db):
    """
    Tests the `check_if_db_exists()` method in `DatabasePostgres`.
    """
    pg_test_db.create_db()
    assert pg_test_db.check_if_db_exists() == True

    pg_test_db.drop_db()
    assert pg_test_db.check_if_db_exists() == False



def test_create_db(pg_test_db):
    """
    Tests the `get_conn()` method in `DatabasePostgres`.  Testing when the
    """
    # Want to ensure db does not exist before starting
    pg_test_db.drop_db()

    # Ensure database does not exist
    with pytest.raises(psycopg2.OperationalError):
        pg_test_db.connect(False)

    # Create the database successfully
    pg_test_db.create_db()
    conn = pg_test_db.connect(False)   # This test is expected to pass
    conn.close()

    # Re-check the non-create path
    pg_test_db.create_db()
    conn = pg_test_db.connect(False)   # This test is expected to pass
    conn.close()



def test_drop_db(pg_test_db):
    """
    Tests the `drop_db()` method in `DatabasePostgres`.
    """
    pg_test_db.create_db()
    assert pg_test_db.check_if_db_exists() == True

    pg_test_db.drop_db()
    assert pg_test_db.check_if_db_exists() == False
