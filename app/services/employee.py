from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models import Employee, Department
from app.schemas import EmployeeCreate


class EmployeeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_employee(self, dept_id: int, schema: EmployeeCreate) -> Employee:
        dept = await self.db.get(Department, dept_id)
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with id {dept_id} not found.",
            )

        db_employee = Employee(**schema.model_dump(), department_id=dept_id)
        self.db.add(db_employee)
        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee
