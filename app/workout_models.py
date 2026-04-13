from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.workout_database import WorkoutBase


class WorkoutLog(WorkoutBase):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, nullable=False, index=True)
    exercise = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=True)
    workout_date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
