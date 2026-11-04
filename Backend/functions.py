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

session = Session(engine)

if session.query(Election).first() is None:
    election_data = Election(phase="nominations")
    session.add(election_data)
    session.commit()

session.close()


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

# Get the current phase. 
def get_current_phase():
    session = Session(engine)
    election_data = session.query(Election).first()
    if election_data is None:
        session.close()
        return None
    current_phase = election_data.phase
    session.close()
    return current_phase

# move to the election next phase
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

# def move_to_next_phase():
#     session =Session(engine)
#     current_phase = session.query(Election).first()
#     if current_phase:
#         if current_phase.phase == "nomination":
#             current_phase.phase = "voting"
#         elif current_phase.phase == "voting":
#             current_phase.phase = "result"
#         elif current_phase.phase == "result":
#             current_phase.phase = "closed"
#     else:
#         current_phase= Election(phase="nomination")
#         session.add(current_phase)
#         phase = current_phase.phase
#     session.commit()
#     session.close()
#     return phase    


#  Cast a vote: voter's roll number and candidate. The position comes from the candidate. 
# Cast a vote
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

# Get positions already voted by a student
def get_positions_voted(voter_roll):
    session = Session(engine)

    voted_positions = session.query(Votes.position).filter(
        Votes.voter_roll == voter_roll
    ).all()

    response = []

    for position in voted_positions:
        response.append(position[0])

    session.close()
    return response

# # getting candidate by candidate id
# def get_candidate_by_id(candidate_id):
#     session = Session(engine)
#     candidate = session.get(Candidates, candidate_id)
#     if candidate is None:
#         session.close()
#         return None
#     candidate_dict = {
#         "id": candidate.id,
#         "roll_no": candidate.roll_no,
#         "name": candidate.name,
#         "position": candidate.position,
#         "mainfesto": candidate.mainfesto,
#         "status": candidate.status,
#         "nominated_on": candidate.nominated_on
#     }
#     session.close()
#     return candidate_dict


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
# Get election results
def get_results():
    session = Session(engine)

    positions = [
        "class_rep",
        "sports_secretary",
        "cultural_secretary",
        "tech_secretary"
    ]

    response = []

    for position in positions:

        candidates = session.query(Candidates).filter(
            Candidates.position == position,
            Candidates.status == "approved"
        ).all()

        candidate_results = []
        highest_votes = -1
        winner = None

        for candidate in candidates:

            total_votes = session.query(Votes).filter(
                Votes.candidate_id == candidate.id
            ).count()

            candidate_data = {
                "candidate_id": candidate.id,
                "roll_no": candidate.roll_no,
                "name": candidate.name,
                "votes": total_votes
            }

            candidate_results.append(candidate_data)

            if total_votes > highest_votes:
                highest_votes = total_votes
                winner = candidate_data

        response.append({
            "position": position,
            "candidates": candidate_results,
            "winner": winner
        })

    session.close()
    return response