from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_path = "Elections.db"
engine = create_engine(f"sqlite:///{DB_path}")
Base = declarative_base()


class Candidates(Base):
    __tablename__ = "Candidates"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    name = Column(String)
    position = Column(String)
    manifesto = Column(String)
    status = Column(String)
    nominated_on = Column(DateTime, default=datetime.now)


class Votes(Base):
    __tablename__ = "Votes"

    id = Column(Integer, primary_key=True)
    position = Column(String)
    candidate_id = Column(Integer, ForeignKey("Candidates.id"))
    voter_roll = Column(String)
    voted_on = Column(DateTime, default=datetime.now)


class Election(Base):
    __tablename__ = "Election"

    id = Column(Integer, primary_key=True)
    phase = Column(String)


Base.metadata.create_all(engine)


# E1 - Get all candidates with filters

def get_all_candidates(position: str = None, approved_only: bool = False):
    session = Session(engine)
    candidates = session.query(Candidates)

    if position is not None:
        candidates = candidates.filter(Candidates.position == position)

    if approved_only is True:
        candidates = candidates.filter(Candidates.status == "approved")
    candidates = candidates.all()
    response = []
    for candidate in candidates:
        candidate_list = {
            "id": candidate.id,
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "manifesto": candidate.manifesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
        response.append(candidate_list)
    session.close()
    return response


# E2 - Get candidate by ID

def get_candidate_by_id(candidate_id: int):
    session = Session(engine)
    candidate = session.query(Candidates).filter(Candidates.id == candidate_id).first()
    if candidate:
        response = {
            "id": candidate.id,
            "roll_no": candidate.roll_no,
            "name": candidate.name,
            "position": candidate.position,
            "manifesto": candidate.manifesto,
            "status": candidate.status,
            "nominated_on": candidate.nominated_on
        }
    else:
        response = None
    session.close()
    return response


# E3 - Nominate a candidate

def nominate_candidate(roll_no: str, name: str, position: str, manifesto: str):
    session = Session(engine)
    candidate = Candidates(
        roll_no=roll_no,
        name=name,
        position=position,
        manifesto=manifesto,
        status="nominated"
    )
    session.add(candidate)
    session.commit()
    response = {
        "id": candidate.id,
        "roll_no": candidate.roll_no,
        "name": candidate.name,
        "position": candidate.position,
        "manifesto": candidate.manifesto,
        "status": candidate.status,
        "nominated_on": candidate.nominated_on
    }
    session.close()
    
    return response


# E4 - Approve a candidate

def approve_candidate(candidate_id: int):
    session = Session(engine)
    candidate = session.query(Candidates).filter(Candidates.id == candidate_id).first()
    if candidate is None:
        session.close()
        return None
    if candidate.status == "nominated":
        candidate.status = "approved"
    session.commit()
    response = {
        "id": candidate.id,
        "roll_no": candidate.roll_no,
        "name": candidate.name,
        "status": candidate.status,
        "position": candidate.position
    }
    session.close()
    return response


# E5 - Withdraw a candidate

def withdraw_candidate(candidate_id: int, roll_no: str):
    session = Session(engine)
    candidate = session.query(Candidates).filter(Candidates.id == candidate_id, Candidates.roll_no == roll_no).first()
    if candidate is None:
        session.close()
        return None
    if candidate.status in ["nominated", "approved"]:
        candidate.status = "withdrawn"
    session.commit()
    response = {
        "id": candidate.id,
        "roll_no": candidate.roll_no,
        "name": candidate.name,
        "status": candidate.status,
        "position": candidate.position
    }
    session.close()
    return response


# E6 - Get current election phase

def get_current_phase():
    session = Session(engine)
    current_phase = session.query(Election).first()
    if current_phase:
        phase = current_phase.phase
    else:
        phase = None
    session.close()
    return phase


# E7 - Move to the next election phase

def move_to_next_phase():
    session = Session(engine)
    current_phase = session.query(Election).first()
    if current_phase is None:
        current_phase = Election(phase="nomination")
        session.add(current_phase)

    elif current_phase.phase == "nomination":
        current_phase.phase = "voting"

    elif current_phase.phase == "voting":
        current_phase.phase = "results"

    elif current_phase.phase == "results":
        current_phase.phase = "closed"
    else:
        current_phase.phase = "nomination"

    session.commit()
    phase = current_phase.phase
    session.close()
    return phase


# E8 - Cast a vote

def cast_vote(voter_roll: str, candidate_id: int):
    session = Session(engine)
    candidate = session.query(Candidates).filter(Candidates.id == candidate_id).first()

    if candidate is None:
        session.close()
        return None

    if candidate.status != "approved":
        session.close()
        return None

    student_votes = session.query(Votes).filter(Votes.voter_roll == voter_roll).all()
    already_voted = False
    for vote in student_votes:
        if vote.position == candidate.position:
            already_voted = True
    if already_voted:
        session.close()
        return None

    new_vote = Votes(
        position=candidate.position,
        candidate_id=candidate.id,
        voter_roll=voter_roll
    )

    session.add(new_vote)
    session.commit()
    response = {
        "vote_id": new_vote.id,
        "position": new_vote.position,
        "candidate_id": new_vote.candidate_id,
        "voter_roll": new_vote.voter_roll,
        "voted_on": new_vote.voted_on
    }
    session.close()
    return response


# E9 - Get positions already voted by a student

def get_student_votes(roll_no: str):
    session = Session(engine)
    votes = session.query(Votes).filter( Votes.voter_roll == roll_no).all()
    voted = []
    for vote in votes:
        if vote.position not in voted:
            voted.append(vote.position)

    session.close()
    return voted


# E10 - Get election results

def get_results():
    session = Session(engine)
    candidates = session.query(Candidates).filter(Candidates.status == "approved").all()

    results = []
    for candidate in candidates:
        total_votes = session.query(Votes).filter(Votes.candidate_id == candidate.id).count()
        candidate_result = {
            "position": candidate.position,
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "votes": total_votes
        }
        results.append(candidate_result)
    session.close()
    return results