from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel

__all__ = ["Donation"]


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
