import pytest
from django.test import Client
from django.db import connections


@pytest.fixture
def client():
    """Fixture providing an test client"""
    return Client()


@pytest.fixture(autouse=True)
def close_db_connections():
    """Ensure all database connections are closed after each test"""
    yield
    for conn in connections.all():
        conn.close()
