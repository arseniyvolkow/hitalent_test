from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import Optional
from app.models import Department, Employee
from app.schemas import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_department(self, schema: DepartmentCreate) -> Department:
        query = select(Department).where(
            Department.name == schema.name, Department.parent_id == schema.parent_id
        )
        result = await self.db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Department with name '{schema.name}' already exists under this parent.",
            )

        if schema.parent_id is not None:
            parent = await self.db.get(Department, schema.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent department with id {schema.parent_id} not found.",
                )

        db_dept = Department(**schema.model_dump())
        self.db.add(db_dept)
        await self.db.commit()
        await self.db.refresh(db_dept)
        return db_dept

    async def get_department(
        self, dept_id: int, depth: int = 1, include_employees: bool = True
    ):
        dept = await self.db.get(Department, dept_id)
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        loaded_dept = await self._load_tree(dept_id, depth, include_employees)
        return self._to_dict(loaded_dept, depth, include_employees)

    def _to_dict(self, dept: Department, depth: int, include_employees: bool) -> dict:
        data = {
            "id": dept.id,
            "name": dept.name,
            "parent_id": dept.parent_id,
            "created_at": dept.created_at,
            "children": [],
            "employees": [] if include_employees else None,
        }

        if include_employees and "employees" in dept.__dict__:
            # Sort employees by created_at as required by ТЗ
            sorted_employees = sorted(dept.employees, key=lambda e: e.created_at)
            data["employees"] = [
                {
                    "id": e.id,
                    "department_id": e.department_id,
                    "full_name": e.full_name,
                    "position": e.position,
                    "hired_at": e.hired_at,
                    "created_at": e.created_at,
                }
                for e in sorted_employees
            ]

        if depth > 0 and "children" in dept.__dict__:
            data["children"] = [
                self._to_dict(child, depth - 1, include_employees)
                for child in dept.children
            ]

        return data

    async def _load_tree(
        self, dept_id: int, depth: int, include_employees: bool
    ) -> Department:
        options = []
        if include_employees:
            options.append(selectinload(Department.employees))

        if depth > 0:
            curr_dept_node = selectinload(Department.children)
            options.append(curr_dept_node)
            if include_employees:
                options.append(curr_dept_node.selectinload(Department.employees))

            # Chain children loading up to depth
            for _ in range(depth - 1):
                curr_dept_node = curr_dept_node.selectinload(Department.children)
                options.append(curr_dept_node)
                if include_employees:
                    options.append(curr_dept_node.selectinload(Department.employees))

        query = select(Department).where(Department.id == dept_id).options(*options)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def update_department(
        self, dept_id: int, schema: DepartmentUpdate
    ) -> Department:
        dept = await self.db.get(Department, dept_id)
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return dept

        new_name = update_data.get("name", dept.name)
        new_parent_id = update_data.get("parent_id", dept.parent_id)

        if "parent_id" in update_data and update_data["parent_id"] is not None:
            if update_data["parent_id"] == dept_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Department cannot be its own parent",
                )

            if await self._is_descendant(dept_id, update_data["parent_id"]):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot move department into its own subtree",
                )

            parent = await self.db.get(Department, update_data["parent_id"])
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Target parent department not found",
                )

        if "name" in update_data or "parent_id" in update_data:
            query = select(Department).where(
                Department.name == new_name,
                Department.parent_id == new_parent_id,
                Department.id != dept_id,
            )
            result = await self.db.execute(query)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Department with name '{new_name}' already exists under target parent.",
                )

        for key, value in update_data.items():
            setattr(dept, key, value)

        await self.db.commit()
        await self.db.refresh(dept)
        return dept

    async def _is_descendant(self, parent_id: int, potential_child_id: int) -> bool:
        curr_id = potential_child_id
        while curr_id:
            dept = await self.db.get(Department, curr_id)
            if not dept or not dept.parent_id:
                break
            if dept.parent_id == parent_id:
                return True
            curr_id = dept.parent_id
        return False

    async def delete_department(
        self, dept_id: int, mode: str, reassign_to_id: Optional[int] = None
    ):
        dept = await self.db.get(Department, dept_id)
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        if mode == "cascade":
            await self.db.delete(dept)
        elif mode == "reassign":
            if not reassign_to_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="reassign_to_department_id is required for reassign mode",
                )

            reassign_to = await self.db.get(Department, reassign_to_id)
            if not reassign_to:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reassign target department not found",
                )

            if reassign_to_id == dept_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot reassign to the same department being deleted",
                )

            await self.db.execute(
                update(Employee)
                .where(Employee.department_id == dept_id)
                .values(department_id=reassign_to_id)
            )

            await self.db.execute(
                update(Department)
                .where(Department.parent_id == dept_id)
                .values(parent_id=reassign_to_id)
            )

            await self.db.delete(dept)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid delete mode"
            )

        await self.db.commit()
