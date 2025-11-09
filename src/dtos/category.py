from typing import List, Optional
from pydantic import Field

from src.dtos.base import BaseDTO, IDMixin, TimestampMixin


class CategoryBase(BaseDTO):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название категории",
        examples=["Технологии", "Образование", "Развлечения"]
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseDTO):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Название категории"
    )


class CategoryResponse(IDMixin, TimestampMixin, CategoryBase):
    pass


class CategoryWithPollsResponse(CategoryResponse):
    polls: List["PollResponse"] = Field(
        default_factory=list,
        description="Список опросов в категории"
    )