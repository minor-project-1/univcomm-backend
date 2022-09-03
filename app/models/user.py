from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db.init_db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_type = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Integer, default=True, nullable=False)
    roll_no = Column(String, nullable=False)

class StudentData(Base):
    __tablename__ = "student_data"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    branch = Column(String)
    semester = Column(String)
    department = Column(String)
    user = relationship("User", backref=backref("student_data", uselist=False))

class FacultyData(Base):
    __tablename__ = "faculty_data"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    designation  = Column(String)
    user = relationship("User", backref=backref("faculty_data", uselist=False))

class AlumniData(Base):
    __tablename__ = "alumni_data"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    branch = Column(String)
    department = Column(String)
    batch = Column(Integer)
    user = relationship("User", backref=backref("alumni_data", uselist=False))