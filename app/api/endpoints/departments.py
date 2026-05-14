from typing import Optional

from fastapi import APIRouter, Query, status

from app.dependencies import DepartmentServiceDependency, EmployeeServiceDependency
from app.schemas import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentTreeResponse,
    DepartmentUpdate,
    EmployeeCreate,
    EmployeeResponse,
)

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post(
    "/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED
)
async def create_department(
    schema: DepartmentCreate,
    service: DepartmentServiceDependency,
):
    return await service.create_department(schema)


@router.get("/{id}", response_model=DepartmentTreeResponse)
async def get_department(
    id: int,
    service: DepartmentServiceDependency,
    depth: int = Query(1, ge=0, le=5),
    include_employees: bool = True,
):
    return await service.get_department(id, depth, include_employees)


@router.patch("/{id}", response_model=DepartmentResponse)
async def update_department(
    id: int,
    schema: DepartmentUpdate,
    service: DepartmentServiceDependency,
):
    return await service.update_department(id, schema)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    id: int,
    service: DepartmentServiceDependency,
    mode: str = Query(..., pattern="^(cascade|reassign)$"),
    reassign_to_department_id: Optional[int] = Query(None),
):
    await service.delete_department(id, mode, reassign_to_department_id)
    return None


@router.post(
    "/{id}/employees/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    id: int,
    schema: EmployeeCreate,
    service: EmployeeServiceDependency,
):
    return await service.create_employee(id, schema)
