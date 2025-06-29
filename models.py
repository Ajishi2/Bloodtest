from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Analysis(Base):
    """Database model for storing blood test analysis results"""
    __tablename__ = "analyses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)  # For future user authentication
    file_name = Column(String(255), nullable=False)
    original_query = Column(Text, nullable=False)
    analysis_result = Column(Text, nullable=False)
    status = Column(String(50), default="completed")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processing_time = Column(Float, nullable=True)  # in seconds
    file_size = Column(Integer, nullable=True)  # in bytes
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, file_name='{self.file_name}', status='{self.status}')>"

class User(Base):
    """Database model for user management (future feature)"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>" 