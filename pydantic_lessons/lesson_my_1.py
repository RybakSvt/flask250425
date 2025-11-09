from typing import Optional

from pip._internal import models
# from pydantic import BaseModel, AliasChoices
#
# class Address(BaseModel):
#     id: int
#     country: str
#     city: str
#     street: str
#     post_code: int
#
# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     is_active: bool
#     address: Address
#
# address_1 = Address(id=1,
#                    country="German",
#                    city="Berlin",
#                    street="2 Awesome St.",
#                    post_code=12341)
#
# vasya = User(
#     id=1,
#     name="Vasya",
#     age=22,
#     is_active=True,
#     address=address_1
# )

#print(vasya)
#
# print(vasya.address.street)


# from pydantic import EmailStr
#
#
# class Address(BaseModel):
#     country: str
#     city: str
#     street: str
#     post_code: str
#
#
# class User(BaseModel):
#     name: str
#     age: int
#     email: EmailStr
#     is_active: bool
#     address: Address
#
#
# json_raw_data = """{
#     "name": "Alice",
#     "age": 25,
#     "email": "alice.j@gmail.com",
#     "is_active": true,
#     "address": {
#         "country": "Germany",
#         "city": "Berlin",
#         "street": "38 Awesome St.",
#         "post_code": "0123"
#     }
# }"""
#
#
# from pydantic import ValidationError
#
#
# try:
#     user = User.model_validate_json(json_raw_data)
#     print(user)
#     print("="*100)
#     print(user.address.street)
#     print(user.model_dump_json(indent=4))    # вернуть из Python в json_объект
# except ValidationError as err:
#     print("Validation Error: ", err)
#______________________________________________________________________________________________________________

# #рассматриваем, как убрать дублирование
#
# from enum import StrEnum
# from datetime import datetime
# from typing import Optional
#
# class TestType(StrEnum):
#     BLOOD = "blood"
#     URINE = "urine"
#     XRAY = "xray"
#     MRI = "mri"
#
# class LabTestBase(BaseModel):
#     patient_id: int
#     test_type: TestType
#     test_date: datetime
#
# class LabTestRequest(LabTestBase):
#     notes: Optional[str] = None
#
# class LabTestResponse(LabTestBase):
#     id: str
#     result: Optional[str]
#     is_completed: bool
#
#     def is_urgent(self) -> bool:
#         pass

#___________________________________________________________________________________________________________

# #from typing import Literal
# from typing import Optional
# from pydantic import Field
#
# class Product(BaseModel):
#     #name: Literal["TV", "Chair", "Lampe"] = Field(min_length=2)   # задали список допустимых значений классом Literal
#     name: str = Field(min_length=2, max_length=54)
#     description: Optional[str] = Field(None, max_length=200)
#     price: float = Field(gt=300)
#     in_stock: bool = Field(True, alias="available", description="Если True - продукт на складе, иначе - продукта нет")
#
# json_data = '''{
#     "name": "TV",
#     "price": 302.2,
#     "available": true
# }'''
#
# product = Product.model_validate_json(json_data)
# print(product.model_dump_json(indent=4))

#____________________________________________________________________
from pydantic import (
    BaseModel,
    field_validator,   #декоратор
    ValidationError,
    Field,
    EmailStr,
    AliasChoices
)

# class User(BaseModel):
#     name: str = Field(min_length=3)
#     age: int = Field(ge=18)
#     email: EmailStr = Field(
#         validation_alias=AliasChoices(
#             'email',
#             'Email',
#             'e-mail',
#             'mail'
#         )
#     )
#
#
#     @field_validator('email')
#     def check_email_domain(cls, value: str):  #value -> test.g@gmail.com
#         allowed_domains = {'gmail.com', 'icloud.com'}
#         raw_domain = value.split('@')[-1]    # -> ['test.g', 'gmal.com']
#
#         if raw_domain not in allowed_domains:
#             raise ValidationError(
#                 f"EMAIL must be from one of the following domains: {','.join(allowed_domains)}"
#             )
#         return value

#_________________________________________________________________________________________________________________

# user = User.model_validate_json('''{}''')
#
# print(user)
#
# user.email = "test"
#
# print(user)

# from typing import List, Optional    #вопросы перед уроком по пройденному
#
# a: List
# b: list
#
#
# class A:
#     model_config = ConfigDict(validate_assignment=True)  # v2 standart
#
#     var: str = Field(default="N/A")
#     var_2: Optional[str] = None
#
#     class Config:  # v1 --> deprecated
#         validate_assignment = True
#_________________________________________________________________________________