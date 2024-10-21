from typing import AsyncGenerator
from config import DB_PORT, DB_NAME, DB_USER, DB_HOST, DB_PASS
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


DATABASE = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    DATABASE,
    echo=True, )

Session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, )


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session_factory() as session:
        yield session



