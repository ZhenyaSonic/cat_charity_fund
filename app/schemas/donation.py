from datetime import datetime
from typing import Optional

from pydantic import Field, NonNegativeInt, StrictBool, BaseModel, validator


class DonationCreate(BaseModel):
    full_amount: NonNegativeInt = Field(..., example=10)
    comment: Optional[str]

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError(
                'сумма пожертвования должна быть целочисленной и больше 0')
        return value


class DonationDB(DonationCreate):
    id: int
    full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperuser(DonationDB):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: StrictBool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
