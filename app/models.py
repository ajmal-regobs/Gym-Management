from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    membership_type = Column(String, nullable=False, default="basic")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
