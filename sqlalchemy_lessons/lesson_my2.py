# user: ich1
# password: ich1_password_ilovedbs
# host: ich-edit.edu.itcareerhub.de
# port: 3306
# database: social_blogs


#шаги для создание объектов таблицы в файле Python
# c помощью библиотеки sqlacodegen_v2 -> в итоге получаем готовые классы
#pip install sqlacodegen_v2
#pip install pymysql
#sqlacodegen_v2<user>:<password>@<host>:<port>/<db_name>
#sqlacodegen_v2<user>:<password>@<host>:<port>/<db_name> --outfile <dir_name>/<new_file_name>
#sqlacodegen_v2 mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edu.itcareerhub.de:3306/social_blog
#sqlacodegen_v2 mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs --outfile sqlalchemy_lessons/social_blogs_models.py

# CRUD
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, model_validator
from sqlalchemy.orm import sessionmaker
from sqlalchemy_lessons.social_blogs_models import User


# Pydantic schema
class UserCreateSchema(BaseModel):
    model_config = {                                       # чтобы Pydantic мог обрабатывать также сырые данные
        "from_attributes": True
    }

    first_name: str = Field(..., max_length=25)
    last_name: str | None = Field(default=None, max_length=30)
    email: EmailStr
    password: str
    repeat_password: str
    phone: str | None = Field(default=None, max_length=45)
    role_id: int

    @model_validator(mode='after')
    def validate_password(self):
        if self.password != self.repeat_password:
            raise ValueError(
                '"password" and "repeat_password" fields must be the same'
            )

        return self

class RoleMiniSchema(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    phone: str | None
    rating: float
    role: RoleMiniSchema | None
    deleted: int
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    users: list[UserResponseSchema]


class BDConnector:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bing=self.engine)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):      #exception trace back
        self.session.close()





