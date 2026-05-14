from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.department import DepartmentService
from app.services.employee import EmployeeService

# Database Session Dependency
SessionDependency = Annotated[AsyncSession, Depends(get_db)]


# Service Dependencies
async def get_department_service(
    db: SessionDependency,
) -> DepartmentService:
    return DepartmentService(db)


async def get_employee_service(db: SessionDependency) -> EmployeeService:
    return EmployeeService(db)


DepartmentServiceDependency = Annotated[
    DepartmentService, Depends(get_department_service)
]
EmployeeServiceDependency = Annotated[EmployeeService, Depends(get_employee_service)]
