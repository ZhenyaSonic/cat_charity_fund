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

# Создание асинхронного движка для работы с базой данных
engine = create_async_engine(settings.database_url)

# Создание фабрики для асинхронных сессий
AsyncSessionLocal: sessionmaker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор для получения асинхронной сессии SQLAlchemy.

    Yields:
        AsyncSession: Асинхронная сессия для работы с базой данных.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
