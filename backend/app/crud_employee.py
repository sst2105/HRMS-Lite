from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import List, Optional
from . import models, schemas
from fastapi import HTTPException, status

def get_employee(db: Session, employee_id: UUID) -> Optional[models.Employee]:
    """Get employee by UUID"""
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_employee_id(db: Session, employee_id: str) -> Optional[models.Employee]:
    """Get employee by employee_id string"""
    return db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()

def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    """Get employee by email"""
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    """Get all employees with pagination"""
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employees_with_stats(db: Session) -> List[dict]:
    """Get all employees with their total present days"""
    employees = db.query(models.Employee).all()
    result = []
    
    for emp in employees:
        present_days = db.query(func.count(models.Attendance.id)).filter(
            models.Attendance.employee_id == emp.id,
            models.Attendance.status == models.AttendanceStatus.PRESENT
        ).scalar() or 0
        
        emp_dict = {
            "id": emp.id,
            "employee_id": emp.employee_id,
            "full_name": emp.full_name,
            "email": emp.email,
            "department": emp.department,
            "total_present_days": present_days
        }
        result.append(emp_dict)
    
    return result

def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    """Create new employee with duplicate checks"""
    # Check for duplicate employee_id
    if get_employee_by_employee_id(db, employee.employee_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with ID '{employee.employee_id}' already exists"
        )
    
    # Check for duplicate email
    if get_employee_by_email(db, employee.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with email '{employee.email}' already exists"
        )
    
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: UUID) -> bool:
    """Delete employee and cascade delete attendance records"""
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    db.delete(employee)
    db.commit()
    return True
