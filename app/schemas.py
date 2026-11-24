from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class LabTestCreate(BaseModel):
    code: str = Field(min_length=2, max_length=20, pattern=r"^[A-Z0-9_]+$")
    name: str = Field(min_length=2, max_length=120)
    category: str = Field(min_length=2, max_length=50)
    price: int = Field(ge=0, le=1_000_000)
    description: str | None = None
    fasting_required: bool = False


class LabTestUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    price: int | None = Field(default=None, ge=0, le=1_000_000)
    description: str | None = None
    fasting_required: bool | None = None
    is_active: bool | None = None


class LabTestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    category: str
    price: int
    description: str | None
    fasting_required: bool
    is_active: bool
    created_at: datetime