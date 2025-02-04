from datetime import datetime
from typing import Optional

from pydantic import (Field, NonNegativeInt, StrictBool, BaseModel, validator)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str]
    full_amount: NonNegativeInt


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError(
                'сумма пожертвования должна быть целочисленной и больше 0')
        return value


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[NonNegativeInt]
    invested_amount: Optional[NonNegativeInt]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[StrictBool]

    @validator('name', allow_reuse=True)
    def name_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError('Имя не может быть пустым')
        return value

    @validator('description', allow_reuse=True)
    def description_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError('Описание не может быть пустым')
        return value

    @validator('full_amount', allow_reuse=True)
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Сумма не может быть пустой')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt = Field(..., example=0, )
    fully_invested: StrictBool = Field(..., example=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
