from datetime import datetime, timezone

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import (
    mapped_column,
    Mapped
)
from src.core.db import db


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),  # сторона Python
        server_default=func.current_timestamp(),  # Сторона Базы данных
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),  # сторона Python
        server_default=func.current_timestamp(),  # Сторона Базы данных
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class Base(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    def to_dict(self):
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }