import asyncio
from tests.config import delete_rows, create_test_tables
import pytest
from fastapi.testclient import TestClient
from app.main import app
from pytest_mock import mocker
from unittest.mock import AsyncMock

@pytest.fixture(autouse=True)
def add_clear_tables():
    asyncio.run(create_test_tables())
    yield
    asyncio.run(delete_rows())

@pytest.fixture
def client(mocker):
    mocker.patch("app.main.create_connection", new_callable=AsyncMock)
    with TestClient(app) as c:
        yield c