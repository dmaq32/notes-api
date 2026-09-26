from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.config import get_db, engine_test
from sqlalchemy import text


import asyncio



client = TestClient(app)

async def create_test_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


AsyncSessionLocalTest = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db_test():
    db = AsyncSessionLocalTest()
    try:
        yield db
    finally:
        await db.close()

app.dependency_overrides[get_db] = get_db_test

async def delete_rows():
    async with engine_test.begin() as conn:
        await conn.execute(text("DELETE FROM notes"))
        await conn.execute(text("DELETE FROM users"))