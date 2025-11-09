# ========================================================================
# ВВЕДЕНИЕ В PYDANTIC И BASEMODEL
# ========================================================================

from pydantic import BaseModel

# Обычный класс Python - просто контейнер для данных
class A:
    ...

# Pydantic модель - автоматически проверяет типы данных и валидирует их
class Address(BaseModel):
    id: int          # Должно быть целым числом
    country: str     # Должно быть строкой
    city: str        # Должно быть строкой
    street: str      # Должно быть строкой
    post_code: int   # Должно быть целым числом


class User(BaseModel):
    id: int          # Уникальный номер пользователя
    name: str        # Имя пользователя
    age: int         # Возраст пользователя
    is_active: bool  # Активен ли пользователь (True/False)
    address: Address # Адрес пользователя (вложенный объект)


# Создаем адрес - pydantic автоматически проверит, что все поля правильного типа
address_1 = Address(
    id=1,
    country="Germany",
    city="Berlin",
    street="2 Awesome St.",
    post_code=123456
)

# Создаем пользователя с адресом
vasya = User(
    id=1,
    name="Vasya",
    age=25,
    is_active=True,
    address=address_1
)

# Выводим весь объект пользователя
print(vasya)

# Получаем доступ к улице через вложенный объект адреса
print(vasya.address.street)
# ========================================================================
# РАБОТА С JSON ДАННЫМИ И ВАЛИДАЦИЯ
# ========================================================================

# Пример JSON данных, которые мы хотим преобразовать в Python объект
"""
{
  "name": "John Doe",
  "age": 22,
  "isEmployed": true,
  "address": {
    "street": "123 Main St",
    "city": "New York"
  },
  "phoneNumbers": ["123-456-7890", "456-789-0123"]
}
"""

from pydantic import EmailStr

# Модель адреса - теперь почтовый индекс строка (может содержать буквы)
class Address(BaseModel):
    country: str
    city: str
    street: str
    post_code: str  # Изменили на str, так как может быть "0123" или "AB123"


class User(BaseModel):
    name: str
    age: int
    email: EmailStr  # EmailStr автоматически проверяет правильность email адреса
    is_active: bool
    address: Address

# JSON строка с данными пользователя
json_raw_data = """{
    "name": "Alice",
    "age": 25,
    "email": "alice.j@gmail.com",
    "is_active": true,
    "address": {
        "country": "Germany",
        "city": "Berlin",
        "street": "38 Awesome St.",
        "post_code": "0123"
    }
}"""

from pydantic import ValidationError

# Пытаемся создать объект из JSON - если что-то не так, получим ошибку
try:
    user = User.model_validate_json(json_raw_data)  # Преобразуем JSON в объект
    print(user)
    print("="*100)
    print(user.model_dump_json(indent=4))  # Преобразуем обратно в красивый JSON
except ValidationError as err:
    print("Validation Error: ", err)  # Если данные неправильные, покажем ошибку
# ========================================================================
# НАСЛЕДОВАНИЕ И ИЗБЕЖАНИЕ ДУБЛИРОВАНИЯ КОДА
# ========================================================================

from dataclasses import asdict
from typing import Optional

from pydantic import BaseModel

from enum import StrEnum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Перечисление типов анализов - ограничиваем возможные значения
class TestType(StrEnum):
    BLOOD = "blood"   # Анализ крови
    URINE = "urine"   # Анализ мочи
    XRAY = "xray"     # Рентген
    MRI = "mri"       # МРТ

# Базовый класс с общими полями для всех анализов
class LabTestBase(BaseModel):
    patient_id: int      # ID пациента
    test_type: TestType  # Тип анализа (только из перечисления выше)
    test_date: datetime  # Дата проведения анализа

# Класс для запроса анализа - наследует от базового и добавляет заметки
class LabTestRequest(LabTestBase):
    notes: Optional[str] = None  # Заметки (необязательное поле, по умолчанию None)

# Класс для ответа с результатами - наследует от базового и добавляет результат
class LabTestResponse(LabTestBase):
    id: str                    # Уникальный ID анализа
    result: Optional[str]      # Результат анализа (может быть None, если еще не готов)
    is_completed: bool         # Завершен ли анализ

    def is_urgent(self):
        # Метод для определения срочности анализа
        ...
# ========================================================================
# ФУНКЦИЯ FIELD - НАСТРОЙКА ПОЛЕЙ
# ========================================================================

from typing import Optional
from pydantic import Field

class Product(BaseModel):
    # Название продукта - должно быть от 2 до 54 символов
    name: str = Field(
        min_length=2,    # Минимум 2 символа
        max_length=54    # Максимум 54 символа
    )
    
    # Описание продукта - необязательное поле, максимум 200 символов
    description: Optional[str] = Field(None, max_length=200)
    
    # Цена - должна быть больше 300
    price: float = Field(gt=300)  # gt = greater than (больше чем)
    
    # Есть ли товар на складе - используем alias для JSON
    in_stock: bool = Field(
        True,                    # Значение по умолчанию
        alias="available",       # В JSON это поле будет называться "available"
        description="Если True -- продукт на складе, иначе -- продукта нет."
    )

# JSON данные - используем alias "available" вместо "in_stock"
json_data = """{
    "name": "Телевизор",
    "price": 301,
    "available": true
}"""

# Создаем объект продукта из JSON
product = Product.model_validate_json(json_data)
print(product.model_dump_json(indent=4))


# ========================================================================
# ДЕКОРАТОР FIELD_VALIDATOR И MODEL_CONFIG
# ========================================================================

from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
    field_validator,
    Field,
    AliasChoices,
    ConfigDict
)

class User(BaseModel):
    # Настройки модели - применяются ко всем полям
    model_config = ConfigDict(
        str_min_length=3,        # Все строки должны быть минимум 3 символа
        validate_assignment=True # Валидация работает даже при изменении полей после создания
    )

    name: str
    surname: str
    age: int = Field(ge=18)  # Возраст должен быть больше или равен 18
    email: EmailStr = Field(
        # Поле email может называться по-разному в JSON
        validation_alias=AliasChoices(
            'email',    # обычное название
            'Email',    # с большой буквы
            'e-mail',   # с дефисом
            'mail'      # сокращенное
        )
    )

    # Кастомный валидатор для email - проверяем домен
    @field_validator('email')
    def check_email_domain(cls, value: str):  # value содержит email, например "test.g@gmail.com"
        allowed_domains = {"gmail.com", "icloud.com"}  # Разрешенные домены
        
        # Разбиваем email по символу @ и берем последнюю часть (домен)
        raw_domain = value.split('@')[-1]  # Из "test.g@gmail.com" получим "gmail.com"

        # Если домен не в списке разрешенных, выбрасываем ошибку
        if raw_domain not in allowed_domains:
            raise ValueError(
                f"Email must be from one of the following domains: {', '.join(allowed_domains)}"
            )
        return value  # Возвращаем значение, если все ОК

    # Старый способ настройки (в Pydantic v1)
    # class Config:
    #     str_min_length = 3
    #     validate_assignment = True # включение валидации даже после создание объекта

    # def foo(self):
    #     ...
    #
    # @classmethod
    # def foo_2(cls):
    #     ...

# Тестируем разные варианты названий поля email
json_data = [
    """{"name": "Andre","age": 21,"email": "a.21@gmail.com"}""",      # Обычное название
    """{"name": "Andre","age": 22,"Email": "a.22@test.com"}""",       # С большой буквы
    """{"name": "Andre","age": 23,"e-mail": "a.23@icloud.com"}""",    # С дефисом
    """{"name": "Andre","age": 24,"mail": "a.24@test.com"}""",        # Сокращенное
]

# Пробуем создать пользователей из разных JSON
try:
    for data in json_data:
        user = User.model_validate_json(data)
        print(user)
except ValidationError as err:
    print(err)

# Создаем пользователя с правильными данными
user = User.model_validate_json('{"name": "Andre", "surname": "Black", "age": 21,"email": "a.21@gmail.com"}')

print(user)

# Пытаемся изменить email на неправильный домен - получим ошибку из-за validate_assignment=True
user.email = "test.gmail@yahoo.com"

print(user)

# ========================================================================
# ДЕКОРАТОР FIELD_VALIDATOR С РЕЖИМАМИ (BEFORE \ AFTER)
# ========================================================================

from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import datetime

class Event(BaseModel):
    # Настройки модели
    model_config = ConfigDict(
        validate_assignment=True,       # Валидация при изменении полей
        str_strip_whitespace=True,      # Автоматически убираем пробелы в начале и конце строк
        json_encoders={                 # Как преобразовывать данные в JSON
            str: lambda v: str(v),      # Строки остаются строками
            int: lambda v: int(v),      # Числа остаются числами
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),  # Даты в формат строки
        }
    )

    title: str
    description: str
    start_date: datetime
    end_date: datetime

    # Валидатор с режимом 'after' - выполняется ПОСЛЕ основной валидации
    @field_validator('end_date', mode='after')
    @classmethod
    def validate_dates(cls, v, info: ValidationInfo):
        # Проверяем, что дата окончания позже даты начала
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError("End date must be after start date")
        return v

# JSON с данными события (заметим лишние пробелы)
event_json = """
{
    "title": "  Annual Developer Conference  ",
    "description": " Meet leading software developers from around the world.  ",
    "start_date": "2025-03-13 15:00:00",
    "end_date": "2025-03-13 18:00:00"
}
"""

# Создание экземпляра события - пробелы автоматически уберутся
event = Event.model_validate_json(event_json)

# Вывод данных события в красивом JSON формате
print(event.model_dump_json(indent=4))

# Попытка изменить end_date на дату до start_date - получим ошибку валидации
try:
    event.end_date = datetime(2025, 3, 13, 14, 40)  # 14:40 раньше чем 15:00
except ValueError as e:
    print(e)
