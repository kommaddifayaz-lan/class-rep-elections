from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return {"message": "Hello World"}

# E1 - get - candidates with position and approved people only

@app.get("/candidates")
def get_candidates(position: str = None, approved_only: bool = False):
    allowed_positions = ["class_rep","sports_secretary","cultural_secretary","tech_secretary"]
    if position is not None and position not in allowed_positions:
        raise HTTPException(status_code=400, detail="Invalid position")
    return function.get_all_candidates(position=position, approved_only=approved_only)

# E2 - get - candidate by id

@app.get("/candidates/{candidate_id}")     
def get_candidate(candidate_id: int):
    candidate = function.get_candidate_by_id(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

# E3 - post - add candidates
@app.post("/candidates")
def add_candidate(roll_no: str, name: str, position: str, mainfesto: str):
    allowed_positions = ["class_rep","sports_secretary","cultural_secretary","tech_secretary"]
    if position not in allowed_positions:
        raise HTTPException(status_code=400, detail="Invalid position")
    phase = function.get_election_phase()
    if phase != "nomination":
        raise HTTPException(status_code=400, detail="Nominations are not currently open")
    return function.add_candidate(roll_no=roll_no, name=name, position=position, mainfesto=mainfesto)

# E4 - PATCH - approve a candidate nomination
@app.patch("/candidates/{candidate_id}/approve")   
def approve_candidate(candidate_id: int):
    phase = function.get_election_phase()
    if phase != "nomination":
        raise HTTPException(status_code=400, detail="Nominations are not currently open")
    candidate = function.get_candidate_by_id(candidate_id)
    if candidate["status"] != "nominated":
        raise HTTPException(status_code=400, detail="Candidate is not nominated")
    if candidate["status"] == "approved":
        raise HTTPException(status_code=400, detail="Candidate is already approved")
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return function.approve_candidate(candidate_id=candidate_id)

# E5 - PATCH - withdraw a candidate nomination

@app.patch("/candidates/{candidate_id}/withdraw")
def withdraw_candidate(candidate_id: int):
    candidate = function.get_candidate_by_id(candidate_id)
    if candidate["status"] != "nominated":
        raise HTTPException(status_code=400, detail="Candidate is not nominated")
    if candidate["status"] == "withdrawn":
        raise HTTPException(status_code=400, detail="Candidate is already withdrawn")
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return function.withdraw_candidate(candidate_id=candidate_id)

# E6 - GET - the current election phase
@app.get("/election/phase")
def get_election_phase():
    return function.get_election_phase()

# E7 - PATCH - move to the next election phase
@app.patch("/election/phase/next")
def move_to_next_phase():
    phase = function.move_to_next_phase()
    if phase == "closed":
        raise HTTPException(status_code=400, detail="Election is already closed")
    return phase

# E8 - POST - cast a vote
@app.post("/votes")
def cast_vote(voter_roll:str, candidaate_id:int):
    phase = function.get_election_phase()
    if phase != "voting":
        raise HTTPException(status_code=400, detail="Voting is not currently open")
    candidate = function.get_candidate_by_id(candidaate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")  
    if candidate["status"] != "approved":
        raise HTTPException(status_code=400, detail="Candidate is not approved")
    return function.cast_vote(voter_roll=voter_roll, candidate_id=candidaate_id)

# E9 - GET - get the positions alredy voted by a voter
@app.get("/votes/{voter_roll}")
def get_positions_voted(voter_roll:str):
    phase = function.get_election_phase()
    if phase != "voting":
        raise HTTPException(status_code=400, detail="Voting is not currently open")
    return function.get_positions_voted(voter_roll=voter_roll)


# E10 - GET - get the results of the election
@app.get("/results")
def get_results():
    phase = function.get_election_phase()
    if phase != "closed":
        raise HTTPException(status_code=403, detail="Election is not closed yet")
    return function.get_results()