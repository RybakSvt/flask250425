# 1.Создать модель минерала для системы управления поставками драгоценных камней.
#
# ТРЕБОВАНИЯ:
# - Уникальный идентификатор (BigInteger, автоинкремент)
# - Название минерала (строка, максимум 50 символов, уникальное)
# - Цвет минерала (строка, максимум 30 символов)
# - Твердость по шкале Мооса (число с плавающей точкой)

# 2.Создать модель салона для системы управления сетью элитных бутиков.
#
# ТРЕБОВАНИЯ:
# - Уникальный идентификатор
# - Название салона (строка, максимум 50 символов)
# - Местоположение салона (строка, максимум 100 символов)
# - Ограничение уникальности: комбинация (название + местоположение) должна быть уникальной

from typing import Optional

from sqlalchemy import String, Integer, create_engine, ForeignKey, Text, Table, Column, BigInteger, Float, \
    UniqueConstraint
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from pathlib import Path


BASE_DIR: Path = Path(__file__).parent   #путь про

#print(BASE_DIR)

DB_PATH: Path = BASE_DIR / 'minerals.db'

engine = create_engine(
    url=f"sqlite:///{DB_PATH}",
    echo=True   # !!! ТОЛЬКО В РЕЖИМЕ ОТЛАДКИ
)

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


class Mineral(Base):
    __tablename__ = "minerals"
    name: Mapped[str] = mapped_column(String(50), unique=True)
    color: Mapped[str] = mapped_column(String(30))
    hardness: Mapped[float] = mapped_column(Float)

class Salon(Base):
    __tablename__ = "salons"
    __table_args__ = (
        UniqueConstraint("name", "location", name="uq_address_salon"),
    )
    name: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(100))



Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

minerals = [Mineral(name="Diamant", color="white", hardness=1.8),
            Mineral(name="Rubin", color="red", hardness=0.8),
            Mineral(name="Opal", color="yellow", hardness=0.5)
]

for mineral in minerals:
    session.add(mineral)

salons = [
    Salon(name="Umka", location="Dorthmund"),
    Salon(name="Bagira", location="Dusseldorf"),
    Salon(name="Valencia", location="Essen")
]

for salon in salons:
    session.add(salon)

session.commit()

session.close()



