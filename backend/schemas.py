import re
from pydantic import BaseModel, Field, field_validator


class RepairBase(BaseModel):
    car_model: str = Field(..., description="Марка и модель авто")
    issue: str = Field(..., description="Описание проблемы")
    estimated_cost: float = Field(..., description="Примерная стоимость ремонта")
    phone_number: str = Field(..., description="Телефон владельца")
    is_completed: bool = Field(default=False, description="Статус готовности")

    @field_validator('car_model')
    @classmethod
    def validate_car(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Марка авто должна содержать минимум 2 символа!')
        return v

    @field_validator('issue')
    @classmethod
    def validate_issue(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Описание проблемы должно быть не короче 3 символов!')
        return v

    @field_validator('estimated_cost')
    @classmethod
    def validate_cost(cls, v):
        if v < 0:
            raise ValueError('Стоимость не может быть отрицательной!')
        return v

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v):
        if re.search(r'[a-zA-Zа-яА-Я]', v):
            raise ValueError('В номере телефона не должно быть букв!')

        digits = re.sub(r'\D', '', v)

        if len(digits) < 10:
            raise ValueError('В номере телефона должно быть минимум 10 цифр!')

        if len(digits) > 11:
            raise ValueError('Номер телефона слишком длинный!')

        return v

class RepairCreate(RepairBase):
    pass


class RepairRead(RepairBase):
    id: int