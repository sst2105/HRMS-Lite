from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from uuid import UUID
from datetime import date
from typing import List, Optional
from . import models, schemas
from fastapi import HTTPException, status

def get_attendance(db: Session, attendance_id: UUID) -> Optional[models.Attendance]:
    """Get attendance record by ID"""
    return db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()

def get_employee_attendance(
    db: Session, 
    employee_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Attendance]:
    """Get all attendance records for an employee"""
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).order_by(models.Attendance.date.desc()).offset(skip).limit(limit).all()

def get_all_attendance(db: Session, skip: int = 0, limit: int = 100) -> List[models.Attendance]:
    """Get all attendance records"""
    return db.query(models.Attendance).order_by(
        models.Attendance.date.desc()
    ).offset(skip).limit(limit).all()

def get_attendance_by_date(db: Session, filter_date: date) -> List[models.Attendance]:
    """Get all attendance records for a specific date"""
    return db.query(models.Attendance).filter(
        models.Attendance.date == filter_date
    ).all()

def get_attendance_by_date_range(
    db: Session, 
    start_date: date, 
    end_date: date
) -> List[models.Attendance]:
    """Get attendance records within a date range"""
    return db.query(models.Attendance).filter(
        and_(
            models.Attendance.date >= start_date,
            models.Attendance.date <= end_date
        )
    ).order_by(models.Attendance.date.desc()).all()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate) -> models.Attendance:
    """Create attendance record with duplicate check"""
    # Check if employee exists
    employee = db.query(models.Employee).filter(
        models.Employee.id == attendance.employee_id
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check for duplicate attendance on same date
    existing = db.query(models.Attendance).filter(
        and_(
            models.Attendance.employee_id == attendance.employee_id,
            models.Attendance.date == attendance.date
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Attendance for employee on {attendance.date} already exists"
        )
    
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    """Get dashboard statistics"""
    from datetime import date as date_class
    today = date_class.today()
    
    total_employees = db.query(func.count(models.Employee.id)).scalar() or 0
    total_attendance = db.query(func.count(models.Attendance.id)).scalar() or 0
    
    present_today = db.query(func.count(models.Attendance.id)).filter(
        and_(
            models.Attendance.date == today,
            models.Attendance.status == models.AttendanceStatus.PRESENT
        )
    ).scalar() or 0
    
    absent_today = db.query(func.count(models.Attendance.id)).filter(
        and_(
            models.Attendance.date == today,
            models.Attendance.status == models.AttendanceStatus.ABSENT
        )
    ).scalar() or 0
    
    return schemas.DashboardStats(
        total_employees=total_employees,
        total_attendance_records=total_attendance,
        present_today=present_today,
        absent_today=absent_today
    )
