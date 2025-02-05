from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Пользователя, наследуемая от SQLAlchemyBaseUserTable.
    """

    def __str__(self):
        return f"User (ID: {self.id})"
