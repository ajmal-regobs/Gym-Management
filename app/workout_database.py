import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

WORKOUT_DATABASE_URL = (
    f"postgresql://{os.getenv('WORKOUT_POSTGRES_USER', 'postgres')}"
    f":{os.getenv('WORKOUT_POSTGRES_PASSWORD', 'postgres')}"
    f"@{os.getenv('WORKOUT_POSTGRES_HOST', 'localhost')}"
    f":{os.getenv('WORKOUT_POSTGRES_PORT', '5432')}"
    f"/{os.getenv('WORKOUT_POSTGRES_DB', 'workouts')}"
)

workout_engine = create_engine(WORKOUT_DATABASE_URL)
WorkoutSessionLocal = sessionmaker(bind=workout_engine)


class WorkoutBase(DeclarativeBase):
    pass


def get_workout_db():
    db = WorkoutSessionLocal()
    try:
        yield db
    finally:
        db.close()
