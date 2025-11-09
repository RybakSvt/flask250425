from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, TimestampMixin


class PollStatistics(Base, TimestampMixin):
    __tablename__ = 'poll_statistics'

    poll_id: Mapped[int] = mapped_column(
        ForeignKey('polls.id'),
        unique=True,
        nullable=False
    )
    total_votes: Mapped[int] = mapped_column(Integer, default=0)
    unique_voters: Mapped[int] = mapped_column(Integer, default=0)

    # Связи
    poll: Mapped["Poll"] = relationship(back_populates="statistics")
    option_stats: Mapped[list["OptionStatistics"]] = relationship(
        back_populates="poll_stats",
        cascade="all, delete-orphan"
    )


class OptionStatistics(Base, TimestampMixin):
    __tablename__ = 'option_statistics'

    poll_stats_id: Mapped[int] = mapped_column(
        ForeignKey('poll_statistics.id'),
        nullable=False
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey('poll_options.id'),
        nullable=False
    )
    votes_count: Mapped[int] = mapped_column(Integer, default=0)
    percentage: Mapped[float] = mapped_column(Float, default=0.0)

    # Связи
    poll_stats: Mapped["PollStatistics"] = relationship(back_populates="option_stats")
    option: Mapped["PollOption"] = relationship()