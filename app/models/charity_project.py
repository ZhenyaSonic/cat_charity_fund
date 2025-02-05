from sqlalchemy import Column, String, Text

from app.models.base import BaseModel


class CharityProject(BaseModel):
    """
    Для благотворительных проектов:
    - name: Название проекта (уникальное).
    - description: Описание проекта.
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return f"CharityProject (ID: {self.id}, Name: {self.name})"
