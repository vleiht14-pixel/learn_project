from pydantic import BaseModel, Field

class RepairCreate(BaseModel):
    car_model: str = Field(..., min_length=2, max_length=100, description="Марка и модель авто")
    issue: str = Field(..., min_length=3, description="Описание проблемы")
    estimated_cost: float = Field(..., ge=0, description="Примерная стоимость ремонта")
    is_completed: bool = Field(default=False, description="Статус готовности")

class RepairUpdate(BaseModel):
    car_model: str
    issue: str
    estimated_cost: float
    is_completed: bool

class RepairRead(BaseModel):
    id: int
    car_model: str
    issue: str
    estimated_cost: float
    is_completed: bool