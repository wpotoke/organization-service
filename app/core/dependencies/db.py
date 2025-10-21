from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as db:
        yield db
