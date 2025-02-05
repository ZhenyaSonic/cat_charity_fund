from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    """
    Для пожертований:
    - user_id: ID пользователя, сделавшего пожертвование.
    - comment: Комментарий к пожертвованию.
    """
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return f"""<Donation(id={self.id},
        user_id={self.user_id},
        full_amount={self.full_amount})>"""

    def __str__(self):
        return f"""Donation (ID: {self.id},
        User ID: {self.user_id},
        Amount: {self.full_amount})"""
