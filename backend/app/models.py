from sqlalchemy import Column, String, Date, Enum, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from .database import Base

class AttendanceStatus(str, enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    
    # Relationship
    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_employee_name', 'full_name'),
        Index('idx_employee_dept', 'department'),
    )

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    
    # Relationship
    employee = relationship("Employee", back_populates="attendance_records")
    
    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_employee_date'),
        Index('idx_attendance_date', 'date'),
        Index('idx_attendance_status', 'status'),
        Index('idx_attendance_employee_date', 'employee_id', 'date'),
    )
