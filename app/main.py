from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Member
from app.schemas import MemberCreate, MemberResponse, WorkoutLogCreate, WorkoutLogResponse
from app.workout_database import WorkoutBase, workout_engine, get_workout_db
from app.workout_models import WorkoutLog

Base.metadata.create_all(bind=engine)
WorkoutBase.metadata.create_all(bind=workout_engine)

app = FastAPI(title="Gym Management API")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/members", response_model=MemberResponse, status_code=201)
def add_member(member: MemberCreate, db: Session = Depends(get_db)):
    existing = db.query(Member).filter(Member.email == member.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Member with this email already exists")
    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@app.delete("/members/{member_id}", status_code=204)
def remove_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()


@app.get("/members", response_model=list[MemberResponse])
def list_members(db: Session = Depends(get_db)):
    return db.query(Member).all()


@app.post("/workouts", response_model=WorkoutLogResponse, status_code=201)
def add_workout_log(workout: WorkoutLogCreate, db: Session = Depends(get_workout_db)):
    db_workout = WorkoutLog(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@app.get("/workouts", response_model=list[WorkoutLogResponse])
def list_workout_logs(
    member_id: int | None = Query(None),
    db: Session = Depends(get_workout_db),
):
    query = db.query(WorkoutLog)
    if member_id is not None:
        query = query.filter(WorkoutLog.member_id == member_id)
    return query.all()


@app.delete("/workouts/{workout_id}", status_code=204)
def delete_workout_log(workout_id: int, db: Session = Depends(get_workout_db)):
    workout = db.query(WorkoutLog).filter(WorkoutLog.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout log not found")
    db.delete(workout)
    db.commit()
