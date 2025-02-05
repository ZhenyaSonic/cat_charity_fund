from typing import AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """
    Базовый класс для всех моделей,
    добавляющий автоматическое создание имени таблицы
    и поле `id` как первичный ключ.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Автоматически генерирует имя таблицы на основе имени класса.
        """
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal: sessionmaker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор для получения асинхронной сессии SQLAlchemy.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
