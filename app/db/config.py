import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

load_dotenv()


def build_database_url(driver: str, database: str | None = None) -> str:
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    if database is None:
        database = os.environ["POSTGRES_DB"]
    return f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"


DATABASE_URL = build_database_url("asyncpg")

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

engine_test = create_async_engine(build_database_url("asyncpg", database="notes-api-tests"), echo=True, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()