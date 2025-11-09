from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Vote(Base, TimestampMixin):
    __tablename__ = 'votes'

    poll_id: Mapped[int] = mapped_column(ForeignKey('polls.id'), nullable=False)
    option_id: Mapped[int] = mapped_column(ForeignKey('poll_options.id'), nullable=False)
    voter_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)  # IPv6 support
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)

    # Связи
    poll: Mapped["Poll"] = relationship(back_populates="votes")
    option: Mapped["PollOption"] = relationship(back_populates="votes")
    voter: Mapped["User"] = relationship(back_populates="votes")