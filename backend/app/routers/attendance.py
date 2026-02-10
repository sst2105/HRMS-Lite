from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

from ..database import get_db
from .. import schemas, crud_attendance

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/", response_model=schemas.AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    """Mark attendance for an employee"""
    return crud_attendance.create_attendance(db=db, attendance=attendance)

@router.get("/", response_model=List[schemas.AttendanceResponse])
def get_all_attendance(
    skip: int = 0, 
    limit: int = 100,
    date_filter: Optional[date] = Query(None, description="Filter by specific date"),
    start_date: Optional[date] = Query(None, description="Filter from date"),
    end_date: Optional[date] = Query(None, description="Filter to date"),
    db: Session = Depends(get_db)
):
    """Get all attendance records with optional date filters"""
    if date_filter:
        return crud_attendance.get_attendance_by_date(db=db, filter_date=date_filter)
    elif start_date and end_date:
        return crud_attendance.get_attendance_by_date_range(
            db=db, start_date=start_date, end_date=end_date
        )
    return crud_attendance.get_all_attendance(db=db, skip=skip, limit=limit)

@router.get("/employee/{employee_id}", response_model=List[schemas.AttendanceResponse])
def get_employee_attendance(
    employee_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get attendance records for a specific employee"""
    return crud_attendance.get_employee_attendance(
        db=db, employee_id=employee_id, skip=skip, limit=limit
    )

@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    return crud_attendance.get_dashboard_stats(db=db)
