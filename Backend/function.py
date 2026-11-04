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


def get_all_candidates():
    session = Session(engine)
    candidates_list = session.query(candidates).all()

    filtered_candidates = []
    for candidate in candidates_list:
        candidate_dict = {
            "id": candidate.id,
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "mainfesto": candidate.mainfesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
        filtered_candidates.append(candidate_dict)
    session.commit()
    session.close()
    return filtered_candidates

# getting candidate by candidate id
def get_candidate_by_id(candidate_id):
    session = Session(engine)
    candidate = session.get(candidates, candidate_id)
    session.commit()
    session.close()
    return candidate




