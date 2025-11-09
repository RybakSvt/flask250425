# Задача 1: Наполнение данными
# Добавьте в базу данных следующие категории и продукты
# Добавление категорий: Добавьте в таблицу categories следующие категории:
#
# Название: "Электроника", Описание: "Гаджеты и устройства."
# Название: "Книги", Описание: "Печатные книги и электронные книги."
# Название: "Одежда", Описание: "Одежда для мужчин и женщин."
#
# Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан
# с соответствующей категорией:
#
# Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
# Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
# Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
# Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
# Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда


from sqlalchemy import create_engine, Integer, String, Numeric, ForeignKey, select, func
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship, joinedload, session
)

from pathlib import Path

BASE_DIR: Path = Path(__file__).parent
DB_PATH: Path = BASE_DIR / 'shop.db'

engine = create_engine(
    url=f"sqlite:///{DB_PATH}",
   # echo=True
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

    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'),
        nullable=True
    )
    category: Mapped['Category'] = relationship(
        "Category",
        back_populates="products"
    )


class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list['Product']] = relationship(
        "Product",
        back_populates="category"
    )


session_factory = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


# def populate_database():
#     """Наполнение базы данных тестовыми данными"""
#
#     with Session(engine) as session:
#         # Проверяем через execute
#         existing_categories = session.execute(select(Category)).scalars().all()
#
#         if existing_categories:
#             print("База данных уже содержит данные. Пропускаем наполнение.")
#             return
#
#         electronics = Category(
#             name="Электроника",
#             description="Гаджеты и устройства.",
#             products=[
#                 Product(name="Смартфон", price=299.99, in_stock=True),
#                 Product(name="Ноутбук", price=499.99, in_stock=True)
#             ]
#         )
#
#         books = Category(
#             name="Книги",
#             description="Печатные книги и электронные книги.",
#             products=[
#                 Product(name="Научно-фантастический роман", price=15.99, in_stock=True)
#             ]
#         )
#
#         clothing = Category(
#             name="Одежда",
#             description="Одежда для мужчин и женщин.",
#             products=[
#                 Product(name="Джинсы", price=40.50, in_stock=True),
#                 Product(name="Футболка", price=20.00, in_stock=True)
#             ]
#         )
#
#         session.add_all([electronics, books, clothing])
#         session.commit()
#         print("База данных успешно наполнена тестовыми данными!")
#
#
# populate_database()


#2
# Задача 2: Чтение данных
# Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты,
# включая их названия и цены.


# with session_factory() as session:
#     stmt = select(Category).options(joinedload(Category.products))
#
#     categories = session.execute(stmt).scalars().unique().all()
#
#     print("=" * 60)
#     print("КАТЕГОРИИ И ПРОДУКТЫ:")
#     print("=" * 60)
#
#     for category in categories:
#         print(f"\nКатегория: {category.name}")
#         print(f"Описание: {category.description}")
#         print("Продукты:")
#
#         if category.products:
#             for product in category.products:
#                 status = "в наличии" if product.in_stock else "нет в наличии"
#                 print(f"  - {product.name}: ${product.price:.2f} ({status})")
#         else:
#             print("  - Нет продуктов в этой категории")
#
#         print("-" * 40)



# Задача 3: Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.

# print("\n" + "=" * 60)
# print("ОБНОВЛЕНИЕ ЦЕНЫ СМАРТФОНА:")
# print("=" * 60)
#
# with session_factory() as session:
#
#     stmt = select(Product).where(Product.name == "Смартфон")
#     smartphone = session.execute(stmt).scalars().first()
#
#     if smartphone:
#         print(f"Найден продукт: {smartphone.name}")
#         print(f"Текущая цена: ${smartphone.price:.2f}")
#
#         smartphone.price = 349.99
#         session.commit()
#
#         print(f"Цена обновлена: ${smartphone.price:.2f}")
#     else:
#         print("Продукт 'Смартфон' не найден")


# Задача 4: Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.

# print("\n" + "=" * 60)
# print("КОЛИЧЕСТВО ПРОДУКТОВ В КАЖДОЙ КАТЕГОРИИ:")
# print("=" * 60)

# with session_factory() as session:
#
#     stmt = select(
#         Category.name,
#         func.count(Product.id).label('product_count')
#     ).join(
#         Product, Category.id == Product.category_id
#     ).group_by(
#         Category.id
#     )
#
#     results = session.execute(stmt).all()
#
#     for category_name, product_count in results:
#         print(f"Категория: {category_name}")
#         print(f"Количество продуктов: {product_count}")
#         print("-" * 40)

# Задача 5: Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.
# Задача 5: Группировка с фильтрацией

# print("\n" + "=" * 60)
# print("КАТЕГОРИИ С БОЛЕЕ ОДНОГО ПРОДУКТА:")
# print("=" * 60)
#
# from sqlalchemy import func
#
# with session_factory() as session:
#
#     stmt = select(
#         Category.name,
#         func.count(Product.id).label('product_count')
#     ).join(
#         Product, Category.id == Product.category_id
#     ).group_by(
#         Category.id
#     ).having(
#         func.count(Product.id) > 1
#     )
#
#     results = session.execute(stmt).all()
#
#     if results:
#         for category_name, product_count in results:
#             print(f"Категория: {category_name}")
#             print(f"Количество продуктов: {product_count}")
#             print("-" * 40)
#     else:
#         print("Нет категорий с более, чем одним продуктом")



