#https://github.com/pareikoVladislav/flask250425
# CRUD

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DataError

from sqlalchemy_lessons.social_blogs_models import User, News
from sqlalchemy_lessons.schemas import UserCreateSchema, UserResponseSchema
from sqlalchemy import create_engine
from sqlalchemy_lessons.db import DBConnector

engine = create_engine(
    url='mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs'
)

def create_user(session, raw_data):
    try:
        validated_data = UserCreateSchema.model_validate_json(raw_data)

        user = User(**validated_data.model_dump())

        session.add(user)
        session.commit()

        return UserResponseSchema.model_validate(user)

    except ValidationError as exc:
        raise ValueError(f"Error: {exc}")

    except (IntegrityError, DataError) as exc:
        session.rollback()

        raise exc

def get_user_by_id(session, user_id):
    user = session.get(User, user_id)

    if not user:
        raise ValueError(
            f"User with ID {user_id} not found"
        )

    return UserResponseSchema.model_validate(user)

from sqlalchemy import select, and_, or_, not_, desc, func

with DBConnector(engine) as session:
    # json_data = """{
    #     "first_name": "Maria",
    #     "last_name": "Gin",
    #     "email": "maria.gin@gmail.com",
    #     "password": "MySecure123Password",
    #     "repeat_password": "MySecure123Password",
    #     "phone": "+1 244 566 8909",
    #     "role_id": 3
    # }"""
    #
    # try:
    #     created_user = create_user(session=session, raw_data=json_data)
    #
    #     print("OUR USER WAS CREATED")
    #     print(created_user)
    # except Exception as err:
    #     print(f"ERROR: {err}")

    # try:
    #     user = get_user_by_id(session=session, user_id=5)
    #
    #     print("USER WAS FOUND")
    #     print(user.model_dump_json(indent=4))
    # except ValueError as exc:
    #     print(exc)

    #smt = select(User) # SELECT *FROM 'users'
    #stmt = select(User).where(User.role_id == 3)    #stmt  - statment (состояние)
    # print("RAW QUERY")
    # print(stmt)
    # print("RAW QUERY")
    # users = session.execute(stmt).scalars().all()      # scalars уберет лишнюю обертку
    #
    # for u in users:             #type: User
    #     print(u.email)

    # stmt = select(User).where(User.rating > 5)
    #
    # print(stmt)
    #
    # data = session.execute(stmt).scalars().all()
    #
    # print(data)
    #
    # resp = [
    #     UserResponseSchema.model_validate(u)
    #     for u in data
    # ]
    # print(resp)

    # stmt = select(User).where(User.rating.between(5, 7))
    #
    # print(stmt)
    #
    # data = session.execute(stmt).scalars().all()
    #
    # print(data)
    #
    # resp = [
    #     UserResponseSchema.model_validate(u)
    #     for u in data
    # ]
    # print(resp)

    # stmt = (
    #     select(User.email, User.role_id, User.rating)
    #     .where(
    #         and_(
    #             User.role_id == 3,
    #             User.rating < 6
    #         )
    #     ).order_by(User.rating)
    # )
    #
    # print(stmt)
    #
    # data = session.execute(stmt).scalars().all()
    #
    # print(data)
    #
    # for u in data:  # type: User
    #     # print(u.email, u.rating, u.role_id)
    #     print(u)

    # stmt = (
    #     select(
    #         User.role_id,
    #         func.avg(User.rating),                       #агрегатная функция через func
    #         #func.count(User.id)
    #     ).group_by(User.role_id)
    # )
    #
    # print(stmt)
    #
    # data = session.execute(stmt).all()
    #
    # print(data)     # результат в виде кортежей

    stmt = (
        select(
            func.count(News.id)
        ).where(
            News.moderated == 1
        )
    )

    print(stmt)

    #data = session.execute(stmt)   #<sqlalchemy.engine.result.ChunkedIteratorResult object at 0x00000206DA0AA690>

    data = session.execute(stmt).scalar()   #  scalar() - для получения одного значения

    print(data)









