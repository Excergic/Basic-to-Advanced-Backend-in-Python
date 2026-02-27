from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from backend.core.config import settings

# Async engine requires an async driver (e.g. asyncpg). Convert postgresql:// to postgresql+asyncpg://
_database_url = settings.DATABASE_URL
if _database_url.startswith("postgresql://"):
    _database_url = _database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
if "?sslmode=" in _database_url:
    _database_url = _database_url.split("?sslmode=")[0]
elif "?ssl=" in _database_url:
    _database_url = _database_url.split("?ssl=")[0]

engine = create_async_engine(
    _database_url,
    echo = False,
    pool_pre_ping = True,
)

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    expire_on_commit = False,
)

class Base(DeclarativeBase):
    pass