from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config.settings import settings

async_engine = create_async_engine(
    settings.database_url,
    echo=settings.sqlalchemy_echo,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={
        "server_settings": {
            "search_path": settings.database_schema
        }
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
