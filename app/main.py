from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Member
from app.schemas import MemberCreate, MemberResponse

Base.metadata.create_all(bind=engine)

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
