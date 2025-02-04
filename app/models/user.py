from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base

__all__ = ["User"]


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя, наследуемая от SQLAlchemyBaseUserTable.
    """

    def __repr__(self):
        return f"<User(id={self.id})>"

    def __str__(self):
        return f"User (ID: {self.id})"
