# Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных,
# обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.
# Задачи:
# Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
# Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные,
# и в случае успеха сериализует объект обратно в JSON и возвращает его.
# Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
# Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи,
# когда валидация не проходит (например возраст не соответствует статусу занятости).
# Модели:
# Address: Должен содержать следующие поля:
# city: строка, минимум 2 символа.
# street: строка, минимум 3 символа.
# house_number: число, должно быть положительным.
# User: Должен содержать следующие поля:
# name: строка, должна быть только из букв, минимум 2 символа.
# age: число, должно быть между 0 и 120.
# email: строка, должна соответствовать формату email.
# is_employed: булево значение, статус занятости пользователя.
# address: вложенная модель адреса.
# Валидация:
# Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
#
# # Пример JSON данных для регистрации пользователя
#

json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""


from pydantic import (
        BaseModel,
        EmailStr,
        AliasChoices,
        Field,
        field_validator,
        ValidationError,
        ConfigDict,
        ValidationInfo
)

class BaseConfigModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

class Address(BaseConfigModel):
    city: str = Field("Not specified", min_length=2)
    street: str = Field("Not specified", min_length=3)
    hause_number: int = Field(default=0, gt=0)


class User(BaseConfigModel):
    name: str = Field(
        ...,
        min_length=2,
        pattern=r"^[A-Za-zÀ-ÿ\s]+$",
        description="Поле включает латинские буквы с акцентами и пробелы)"
)
    age: int = Field(..., gt=0, le=120)
    email: EmailStr = Field(
        ...,
        validation_alias=AliasChoices(
            'email',
            'Email',
            'e-mail',
            'mail'
        )
    )
    is_employed: bool = Field(...)
    address: Address

    @field_validator('is_employed', mode='after')
    def check_employed(cls, value: bool, info: ValidationInfo) -> bool:
        if 'age' in info.data:
            age = info.data['age']
            if (age < 18 or age > 65) and value:
                raise ValueError('Для работы возраст должен быть от 18 до 65 лет')
        return value


try:
    user = User.model_validate_json(json_input)
    print(user.model_dump_json(indent=4))

except ValidationError as err:
    print(f"Validation error: {err}")



# # Ошибка: поле street содержит меньше 3x символов
# json_input = """{
#     "name": "Charles",
#     "age": 40,
#     "email": "charles@example.com",
#     "is_employed": true,
#     "address": {
#         "street": "St",
#         "hause_number": 11
#     }
# }"""


# # Ошибка: отрицательное значение номера дома
# json_input = """{
#     "name": "Anna Maria",
#     "age": 30,
#     "email": "anna@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "Köln",
#         "street": "Bonner",
#         "hause_number": -25
#     }
# }"""


# # Ошибка: имя ключает апостроф
# json_input = """{
#     "name": "John O'Connor",
#     "age": 25,
#     "email": "john@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "New York",
#         "street": "5th Avenue",
#         "hause_number": 123
#     }
# }"""

# # Успешная регистрация с альтернативным email полем
# json_input = """{
#     "name": "Sophie",
#     "age": 29,
#     "Email": "sophie@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "Vienna",
#         "street": "Ringstraße",
#         "hause_number": 55
#     }
# }"""



# Успешная регистрация (граничный случай 18 лет)
# json_input = """{
#     "name": "Lucas",
#     "age": 18,
#     "email": "lucas@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "Amsterdam",
#         "street": "Damrak",
#         "hause_number": 44
#     }
# }"""

# # Успешная регистрация (граничный случай 65 лет)
# json_input = """{
#     "name": "Elena",
#     "age": 65,
#     "email": "elena@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "Prague",
#         "street": "Wenceslas Square",
#         "hause_number": 77
#     }
# }"""

# # Ошибка: работает в 17 лет
# json_input = """{
#     "name": "Jean Claude",
#     "age": 17,
#     "email": "jean@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "Lyon",
#         "street": "Rue de la République",
#         "hause_number": 15
#     }
# }"""

# # Ошибка: работает в 66 лет
# json_input = """{
#     "name": "Robert",
#     "age": 66,
#     "email": "robert@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "Berlin",
#         "street": "Friedrichstraße",
#         "hause_number": 78
#     }
# }"""

# # Успешная регистрация (работает, возраст в диапазоне)
# json_input = """{
#     "name": "John Connor",
#     "age": 25,
#     "email": "john@example.com",
#     "is_employed": true,
#     "address": {
#         "city": "New York",
#         "street": "5th Avenue",
#         "hause_number": 123
#     }
# }"""

# # Успешная регистрация (не работает, возраст любой)
# json_input = """{
#     "name": "Marie José",
#     "age": 70,
#     "email": "marie@example.com",
#     "is_employed": false,
#     "address": {
#         "city": "Paris",
#         "street": "Champs-Élysées",
#         "hause_number": 45
#     }
# }"""









