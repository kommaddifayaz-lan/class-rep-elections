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

class votes(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    position = Column(String)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    voter_roll = Column(String)
    voted_on = Column(DateTime, default=datetime.now())

class election(Base):
    __tablename__ = "election"
    id = Column(Integer, primary_key=True)
    phase = Column(String)

Base.metadata.create_all(engine)


# getting all candidates with their positions and approved people only
def get_all_candidates():
    session = Session(engine)
    candidates = session.query(Candidates).all()
    response = []
    for candidate in candidates:
        candidate_list = {
            "id":candidate.id,
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "mainfesto": candidate.mainfesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
        response.append(candidate_list)
    session.commit()
    session.close()
    return response

# getting candidate by candidate id

def get_candidate_by_id(candidate_id):
    session = Session(engine)
    candidate = session.query(Candidates).filter(Candidates.id == candidate_id).first()
    response = []
    if candidate:
        candidate_data = {
            "id": candidate.id,
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "mainfesto": candidate.mainfesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
        response.append(candidate_data)
    session.commit()
    session.close()
    return response

# nominating a candidate
def nominate_candidate(roll_no, name, position, manifesto):
    session = Session(engine)
    candidate = Candidates(roll_no=roll_no, name=name, position=position, mainfesto=manifesto, status="pending")
    session.add(candidate)
    response = {      
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "mainfesto": candidate.mainfesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
    
    session.commit()
    session.close()
    return response

# move to the election next phase
def move_to_next_phase():
    session =Session(engine)
    current_phase = session.query(election).first()
    next_phase = ""
    if current_phase:
        if current_phase.phase == "nomination":
            next_phase = "voting"
        elif current_phase.phase == "voting":
            next_phase = "result"
        else:
            next_phase = "nomination"
        current_phase.phase = next_phase

    session.commit()
    session.close()


#  Cast a vote: voter's roll number and candidate. The position comes from the candidate. 
def cast_vote(voter_roll, candidate_id):
    session =session(engine)
    candidate = session.query(Candidates).filter(Candidates.id == candidate_id).first()
    if candidate:
        vote = votes(position=candidate.position, candidate_id=candidate.id, voter_roll=voter_roll)
        session.add(vote)
        response = {
            "vote_id": vote.id,
            "position": vote.position,
            "candidate_id": vote.candidate_id,
            "voter_roll": vote.voter_roll,
            "voted_on": vote.voted_on
        }
    session.commit()
    session.close()
    return response




