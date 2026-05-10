from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base

class Location(Base):
    __tablename__ = "locations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True, nullable=False)
    zone = Column(String(50))
    capacity = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)