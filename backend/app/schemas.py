from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional, List
from uuid import UUID
from enum import Enum

class AttendanceStatusEnum(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('employee_id', 'full_name', 'department')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip()

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: UUID
    
    class Config:
        from_attributes = True

class EmployeeWithStats(EmployeeResponse):
    total_present_days: int = 0

# Attendance Schemas
class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatusEnum
    
    @field_validator('date')
    @classmethod
    def validate_date_not_future(cls, v: date) -> date:
        from datetime import date as date_class
        if v > date_class.today():
            raise ValueError('Attendance date cannot be in the future')
        return v

class AttendanceCreate(AttendanceBase):
    employee_id: UUID

class AttendanceResponse(AttendanceBase):
    id: UUID
    employee_id: UUID
    
    class Config:
        from_attributes = True

class AttendanceWithEmployee(AttendanceResponse):
    employee: EmployeeResponse

# Dashboard Schema
class DashboardStats(BaseModel):
    total_employees: int
    total_attendance_records: int
    present_today: int
    absent_today: int
