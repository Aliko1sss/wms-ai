from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    track_expiry = Column(Boolean, default=False)
    attributes = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)