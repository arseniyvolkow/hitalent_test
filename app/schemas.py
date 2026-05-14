from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, date
from typing import Optional, List


class EmployeeBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    position: str = Field(..., min_length=1, max_length=200)
    hired_at: Optional[date] = None

    @field_validator("full_name", "position")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    department_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    parent_id: Optional[int] = Field(None, gt=0)

    @field_validator("name")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    parent_id: Optional[int] = Field(None, gt=0)

    @field_validator("name")
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip()
        return v


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentTreeResponse(DepartmentResponse):
    employees: Optional[List[EmployeeResponse]] = None
    children: List["DepartmentTreeResponse"] = []

    model_config = ConfigDict(from_attributes=True)
