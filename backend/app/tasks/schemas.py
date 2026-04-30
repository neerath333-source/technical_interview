from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None)

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed_statuses = ['pending', 'in-progress', 'completed']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of {allowed_statuses}')
        return v
