from datetime import date, datetime

from pydantic import BaseModel


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


class WorkoutLogCreate(BaseModel):
    member_id: int
    exercise: str
    sets: int
    reps: int
    weight_kg: float | None = None
    workout_date: date
    notes: str | None = None


class WorkoutLogResponse(BaseModel):
    id: int
    member_id: int
    exercise: str
    sets: int
    reps: int
    weight_kg: float | None
    workout_date: date
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
