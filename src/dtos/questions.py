from datetime import datetime
from typing import Optional, List, Self

from pydantic import Field, model_validator

from src.dtos.base import BaseDTO, IDMixin, TimestampMixin


class PollOptionCreateRequest(BaseDTO):
    text: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )


class PollCreateRequest(BaseDTO):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True
    is_anonymous: bool = True
    category_id: int = Field(
        ...,
        gt=0,
        description="ID категории"
    )
    options: List[PollOptionCreateRequest] = Field(
        ...,
        min_length=2,
    )

    @model_validator(mode='after')
    def validate_end_date(self) -> Self:
        if self.end_date is not None and self.end_date <= self.start_date:
            raise ValueError("Дата окончания должна быть позже даты начала")
        return self


class PollUpdateRequest(BaseDTO):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    is_anonymous: Optional[bool] = None
    category_id: Optional[int] = Field(None, gt=0)

    @model_validator(mode='after')
    def validate_end_date(self) -> Self:
        if self.end_date is not None and self.start_date is not None:
            if self.end_date <= self.start_date:
                raise ValueError("Дата окончания должна быть позже даты начала")
        return self


class PollOptionResponse(IDMixin, TimestampMixin):
    poll_id: int = Field(..., gt=0)
    text: str


class PollResponse(IDMixin, TimestampMixin):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True
    is_anonymous: bool = True
    category_id: int = Field(..., gt=0)
    options: List[PollOptionResponse] = Field(default_factory=list)
    #category: Optional["CategoryResponse"] = Field(None, description="Информация о категории")
    category: Optional[dict] = Field(None, description="Информация о категории")

# Для избежания циклических импортов
#from src.dtos.category import CategoryResponse
