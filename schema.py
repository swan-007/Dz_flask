from typing import Optional

from pydantic import BaseModel, validator

from models import Session, User


class CreateAdvertisement(BaseModel):
    heading: str
    description: str
    user_id: int

    @validator("user_id")
    def user_se(cls, value):
        with Session() as s:
            user = s.get(User, value)
            if user is None:
                raise ValueError("Такого пользователя нет")
            return value


class UpdateAdvertisement(BaseModel):
    heading: Optional[str]
    description: Optional[str]
    user_id: Optional[int]

    @validator("user_id")
    def user_se(cls, value):
        with Session() as s:
            user = s.get(User, value)
            if user is None:
                raise ValueError("Такого пользователя нет")
            return value
