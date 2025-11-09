# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение
# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.

from sqlalchemy import create_engine, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

engine = create_engine(
    url='sqlite:///:memory:',
    echo=True
)


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


class Product(Base):
    __tablename__ = 'products'
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(8, 2))
    in_stock: Mapped[bool] = mapped_column(default=True)

    # Связь с категорией
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('categories.id'),
        nullable=True                                 #необязательное поле
    )
    category: Mapped['Category'] = relationship(
        "Category",
        back_populates="products"
    )


class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    # Обратная связь с продуктами
    products: Mapped[list['Product']] = relationship(
        "Product",
        back_populates="category"
    )


session = sessionmaker(bind=engine)()
Base.metadata.create_all(bind=engine)



# # Демонстрация работы
# # Создаем категории
# electronics = Category(
#     name="Электроника",
#     description="Техника и гаджеты"
# )
#
# books = Category(
#     name="Книги",
#     description="Художественная литература"
# )
#
# # Создаем продукты
# laptop = Product(
#     name="Ноутбук",
#     price=999.99,
#     in_stock=True,
#     category=electronics  # Устанавливаем связь
# )
#
# smartphone = Product(
#     name="Смартфон",
#     price=499.99,
#     in_stock=True,
#     category=electronics  # Устанавливаем связь
# )
#
# novel = Product(
#     name="Роман",
#     price=19.99,
#     in_stock=False,
#     category=books  # Устанавливаем связь
# )
#
# # Добавляем все объекты в сессию
# session.add_all([electronics, books, laptop, smartphone, novel])
# session.commit()
#
# # Проверяем связи
# print("\n=== ПРОВЕРКА СВЯЗЕЙ ===")
#
# # Получаем все категории
# categories = session.query(Category).all()
# for category in categories:
#     print(f"\nКатегория: {category.name}")
#     print(f"Описание: {category.description}")
#     print("Продукты в категории:")
#     for product in category.products:
#         print(f"  - {product.name} ({product.price}₽)")
#
# # Получаем все продукты
# print("\n=== ВСЕ ПРОДУКТЫ ===")
# products = session.query(Product).all()
# for product in products:
#     category_name = product.category.name if product.category else "Без категории"
#     print(f"{product.name} - {product.price}₽ - Категория: {category_name}")
#
# # Закрываем сессию
# session.close()