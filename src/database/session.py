from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.utils.config import EnvVariableManager

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{EnvVariableManager.get_env_variable('POSTGRES_USER')}:"
    f"{EnvVariableManager.get_env_variable('POSTGRES_PASSWORD')}@"
    f"{EnvVariableManager.get_env_variable('POSTGRES_HOST')}:"
    f"{EnvVariableManager.get_env_variable('POSTGRES_PORT')}/"
    f"{EnvVariableManager.get_env_variable('POSTGRES_DB')}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
