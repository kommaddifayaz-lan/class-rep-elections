from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import date, datetime

DB_path = "Elections.db"
engine = create_engine(f"sqlite:///{DB_path}")
Base = declarative_base()

class candidates(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    name = Column(String)
    position = Column(String)
    mainfesto = Column(String)
    status = Column(String)
    nominated_on = Column(DateTime, default=datetime.now())

class votes(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    position = Column(String)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    voter_roll = Column(String),
    voted_on = Column(DateTime, default=datetime.now())

class election(Base):
    __tablename__ = "election"
    id = Column(Integer, primary_key=True)
    phase = Column(String)

Base.metadata.create_all(engine)

