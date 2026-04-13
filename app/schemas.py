from datetime import datetime

from pydantic import BaseModel, EmailStr


class MemberCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    membership_type: str = "basic"


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    membership_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
