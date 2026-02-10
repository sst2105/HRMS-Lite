from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from .. import schemas, crud_employee

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    return crud_employee.create_employee(db=db, employee=employee)

@router.get("/", response_model=List[schemas.EmployeeResponse])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all employees"""
    return crud_employee.get_employees(db=db, skip=skip, limit=limit)

@router.get("/with-stats", response_model=List[schemas.EmployeeWithStats])
def get_employees_with_stats(db: Session = Depends(get_db)):
    """Get all employees with their total present days"""
    return crud_employee.get_employees_with_stats(db=db)

@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: UUID, db: Session = Depends(get_db)):
    """Get employee by ID"""
    employee = crud_employee.get_employee(db=db, employee_id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: UUID, db: Session = Depends(get_db)):
    """Delete an employee"""
    crud_employee.delete_employee(db=db, employee_id=employee_id)
    return None
