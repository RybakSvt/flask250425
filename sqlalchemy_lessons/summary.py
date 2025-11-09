# """
# Получить всех пользователей-авторов с рейтингом больше 5
# ТЗ:
#
# Вывести id, first_name, rating.
# """
##работаем с social_blogs_models

from sqlalchemy import create_engine
from sqlalchemy_lessons.social_blogs_models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy_lessons.db import DBConnector

engine = create_engine(
    url='mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs'
)

session = sessionmaker(bind=engine)()

from sqlalchemy import select, and_

with (DBConnector(engine) as session):

    stmt = select(
        User.id, User.first_name, User.rating
    ).where(and_(User.rating > 5, User.role_id == 3))

    data = session.execute(stmt).all()

    for u in data:  # type: User
        print(u.id, u.first_name, u.rating)


    print(data)

# session.close()    # если нет контекстного менеджера

