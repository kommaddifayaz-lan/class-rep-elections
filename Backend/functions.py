from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import date, datetime

DB_path = "Elections.db"
engine = create_engine(f"sqlite:///{DB_path}")
Base = declarative_base()

class Candidates(Base):
    __tablename__ = "Candidates"
    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    name = Column(String)
    position = Column(String)
    mainfesto = Column(String)
    status = Column(String)
    nominated_on = Column(DateTime, default=datetime.now())

class Votes(Base):
    __tablename__ = "Votes"
    id = Column(Integer, primary_key=True)
    position = Column(String)
    candidate_id = Column(Integer, ForeignKey("Candidates.id"))
    voter_roll = Column(String),
    voted_on = Column(DateTime, default=datetime.now())

class Election(Base):
    __tablename__ = "Election"
    id = Column(Integer, primary_key=True)
    phase = Column(String)

Base.metadata.create_all(engine)


def get_all_candidates():
    session = Session(engine)
    candidates_list = session.query(Candidates).all()

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
    candidate = session.get(Candidates, candidate_id)
    if candidate is None:
        session.close()
        return None
    candidate_dict = {
        "id": candidate.id,
        "roll_no": candidate.roll_no,
        "name": candidate.name,
        "position": candidate.position,
        "mainfesto": candidate.mainfesto,
        "status": candidate.status,
        "nominated_on": candidate.nominated_on
    }
    session.close()
    return candidate_dict


# approving a nomination 
def approve_candidate(candidate_id):
    session = Session(engine)
    candidate = session.get(Candidates, candidate_id)
    candidate.status = "approved"
    session.commit()
    candidate_dict = {
        "id": candidate.id,
        "roll_no": candidate.roll_no,
        "name": candidate.name,
        "position": candidate.position,
        "mainfesto": candidate.mainfesto,
        "status": candidate.status,
        "nominated_on": candidate.nominated_on
    }
    session.close()
    return candidate_dict

# Withdraw a nomination, with the candidate's roll number. 

# Withdraw a nomination, with the candidate's roll number. 
def withdraw_candidate(roll_no):
    session = Session(engine)
    candidates_list = session.query(Candidates).filter(Candidates.roll_no == roll_no).all()
    updated_candidates = []
    for candidate in candidates_list:
        candidate.status = "withdrawn"
        session.commit()
        candidate_dict = {
            "id": candidate.id,
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "manifesto": candidate.mainfesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
        updated_candidates.append(candidate_dict)
    session.close()
    return updated_candidates

# Get the current phase. 
def get_current_phase():
    session = Session(engine)

    current_phase = session.query(Election).first()

    if current_phase is not None:
        phase = current_phase.phase
    else:
        phase = None

    session.close()
    return phase