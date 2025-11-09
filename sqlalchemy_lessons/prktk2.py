from sqlalchemy import create_engine, func, desc
from sqlalchemy_lessons.social_blogs_models import User, Role, News
from sqlalchemy_lessons.db import DBConnector

engine = create_engine(
    url='mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs'
)


from sqlalchemy import select, and_

with (DBConnector(engine) as session):

    # 1
    """
    Получить список всех пользователей с их ролями
    ТЗ:

    Вывести id, first_name, last_name, email и name роли.
    Использовать join(User.role).
    """

    # stmt = select(
    #     User.id, User.first_name, User.last_name, Role.name
    # ).join(Role, User.role_id==Role.id)
    #
    # data = session.execute(stmt).all()
    #
    # print(f"{'ID':<5} {'First Name':<15} {'Last Name':<16} {'Role':<10}")
    # print("-" * 50)
    #
    #
    # for id, first_name, last_name, role in data:
    #     print(f"{id:<5} {first_name:<15} {last_name:<16} {role:<10}")

    # 2
    """
    Найти автора с наибольшим количеством новостей
    ТЗ:

    Вывести author_id, количество новостей.
    Группировка по author_id.
    Сортировка по количеству новостей DESC.
    Ограничить 1.
    """

    # stmt = (
    #     select(News.author_id, func.count(News.id))
    #     .where(User.role_id == 3)
    #     .group_by(News.author_id)
    #     .join(User)
    #     .order_by(desc(func.count(News.id)))
    #
    # )
    #
    # data = session.execute(stmt).first()     # вместо all - first
    # print(f"author_id: {data[0]} count_news: {data[1]}" )

    #3
    """
    Вывести средний рейтинг всех пользователей
    ТЗ:

    Вывести средний рейтинг.
    """

    stmt = select(func.avg(User.rating)).where(User.role_id == 3)

    data = session.execute(stmt).scalar()

    print(f"Средний рейтинг всех пользователей: {data:.2f}")

    #4
    """
    Найти пользователей, у которых рейтинг выше среднего
    ТЗ:
    
    Вывести id, first_name, rating.
    """

    stmt1 = select(User.id, User.first_name, User.last_name, User.rating
                   ).where(User.rating > data).order_by(desc(User.rating))


    data_1 = session.execute(stmt1).all()

    print("\nПользователи, у которых рейтинг выше среднего:\n")
    print(f"{'ID':<5} {'First Name':<15} {'Last Name':<19} {'Rating':<8}")
    print("-" * 50)


    for id, first_name, last_name, rating, in data_1:
        print(f"{id:<5} {first_name:<15} {last_name:<19} {rating:<8} ")






