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
    voter_roll = Column(String)
    voted_on = Column(DateTime, default=datetime.now())

class Election(Base):
    __tablename__ = "Election"
    id = Column(Integer, primary_key=True)
    phase = Column(String)

Base.metadata.create_all(engine)


def get_all_candidates(position=None, approved_only: bool = False):
    session = Session(engine)
    candidates = session.query(Candidates)
    if position is not None:
        candidates = candidates.filter(Candidates.position == position)
    if approved_only:
        candidates = candidates.filter(Candidates.status == "approved")
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

# E2 - get - candidates by candidate by id

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


# E3 - Post - add candidates

def nominate_candidate(roll_no, name, position, manifesto):
    session = Session(engine)
    candidate = Candidates(roll_no=roll_no, name=name, position=position, mainfesto=manifesto, status="nominated")
    session.add(candidate)
    session.commit()
    response = { 
            "id": candidate.id,     
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "mainfesto": candidate.mainfesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
    
    
    session.close()
    return response

#E4 - PUT - approve a nomination 

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


# E5 - PATCH - withdraw a nomination 

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


# E6 - GET - Get the current phase. 

def get_current_phase():
    session = Session(engine)

    current_phase = session.query(Election).first()

    if current_phase is not None:
        phase = current_phase.phase
    else:
        phase = None

    session.close()
    return phase


# E7 - PUT - Move to the election next phase

def move_to_next_phase():
    session =Session(engine)
    current_phase = session.query(Election).first()
    next_phase = ""
    if current_phase:
        if current_phase.phase == "nomination":
            next_phase = "voting"
        elif current_phase.phase == "voting":
            next_phase = "closed" 
        else:
            next_phase = "nomination"
        current_phase.phase = next_phase

    session.commit()
    session.close()
    return next_phase




# E8 - POST - Cast a vote

def cast_vote(voter_roll, candidate_id):
    session = Session(engine)

    candidate = session.query(Candidates).filter(
        Candidates.id == candidate_id
    ).first()

    if candidate is None:
        session.close()
        return None

    vote = Votes(
        position=candidate.position,
        candidate_id=candidate.id,
        voter_roll=voter_roll
    )

    session.add(vote)
    session.commit()
    session.refresh(vote)

    response = {
        "vote_id": vote.id,
        "position": vote.position,
        "candidate_id": vote.candidate_id,
        "voter_roll": vote.voter_roll,
        "voted_on": vote.voted_on
    }

    session.close()
    return response

# E9 - GET - Get positions already voted by a student

def get_student_votes(roll_no):
    session = Session(engine)
    votes = session.query(votes).filter(votes.voter_roll == roll_no).all()
    voted = []
    for vote in votes:
        if vote.position not in voted:
            voted.append(vote.position)
    session.close()
    return voted

# E10 - GET - results of the election
def get_results():
    session =Session(engine)
    candidates = session.query(Candidates).filter(Candidates.status == "approved").all()
    results = []
    for candidate in candidates:
        total_votes = session.query(Votes).filter(
            Votes.candidate_id == candidate.id).count()
        results={
            "position": candidate.position,
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "votes": total_votes
        }
        results.append(results)
    session.close()
    return results