from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# PostgreSQL 异步数据库 URL
ASYNC_DATABASE_URL = (
    "postgresql+asyncpg://postgres:1234@localhost:5432/news_app"
)

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,          # 输出 SQL 日志
    pool_size=10,       # 连接池中保持的持久连接数
    max_overflow=20,    # 允许创建的额外连接数
    pool_pre_ping=True  # 使用连接前检查连接是否有效
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# FastAPI 依赖项：获取数据库会话
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise