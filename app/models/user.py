from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base

__all__ = ["User"]


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
