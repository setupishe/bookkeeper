from bookkeeper.repository.sqlite_repository import SQLiteRepository
from test_memory_repository import *
import pytest
import os

DB_NAME = 'test.db'


@pytest.fixture
def repo(custom_class):
    if os.path.isfile(DB_NAME):
        os.remove(DB_NAME)
    return SQLiteRepository(DB_NAME, custom_class)


