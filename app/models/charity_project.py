from sqlalchemy import Column, String, Text

from app.models.base import BaseModel

__all__ = ["CharityProject"]


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
