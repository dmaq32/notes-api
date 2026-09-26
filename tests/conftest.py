import asyncio
from tests.config import delete_rows
import pytest

@pytest.fixture(autouse=True)
def clear_tables():
    yield
    asyncio.run(delete_rows())