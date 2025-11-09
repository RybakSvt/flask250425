# Pydantic schema
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, model_validator


class UserCreateSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

    first_name: str = Field(..., max_length=25)
    last_name: str | None = Field(default=None, max_length=30)
    email: EmailStr
    password: str
    repeat_password: str
    phone: str | None = Field(default=None, max_length=45)
    role_id: int

    @model_validator(mode='after')
    def validate_password(self):
        if self.password != self.repeat_password:
            raise ValueError(
                '"password" and "repeat_password" fields must be the same'
            )

        return self


class RoleMiniSchema(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    phone: str | None
    rating: float
    role: RoleMiniSchema | None
    deleted: int
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    users: list[UserResponseSchema]
