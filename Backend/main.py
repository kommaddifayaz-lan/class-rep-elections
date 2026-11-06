from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import  functions

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

@app.get("/Candidates")
def get_candidates(position: str = None, approved_only: bool = False):
    allowed_positions = ["class_rep","sports_secretary","cultural_secretary","tech_secretary"]
    if position is not None and position not in allowed_positions:
        raise HTTPException(status_code=422, detail="Invalid position")
    return functions.get_all_candidates(position=position, approved_only=approved_only)


# E2 - get - candidate by id

@app.get("/Candidates/{candidate_id}")     
def get_candidate(candidate_id):
    candidate = functions.get_candidate_by_id(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# E3 - post - add candidates

@app.post("/Candidates")
def add_candidate(roll_no, name, position, manifesto):
    allowed_positions = ["class_rep","sports_secretary","cultural_secretary","tech_secretary"]
    if position not in allowed_positions:
        raise HTTPException(status_code=422, detail="Invalid position")
    phase = functions.get_current_phase()
    if phase != "nomination":
        raise HTTPException(status_code=400, detail="Nominations are not currently open")
    return functions.nominate_candidate(roll_no=roll_no, name=name, position=position, manifesto=manifesto)


# E4 - PATCH - approve a candidate nomination

@app.patch("/Candidates/{candidate_id}/approve")   
def approve_candidate(candidate_id):
    phase = functions.get_current_phase()
    if phase != "nomination":
        raise HTTPException(status_code=400, detail="Nominations are not currently open")
    candidate = functions.get_candidate_by_id(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if candidate["status"] == "approved":
            raise HTTPException(status_code=400, detail="Candidate is already approved")
    if candidate["status"] != "nominated":
            raise HTTPException(status_code=400, detail="Candidate is not nominated")
    return functions.approve_candidate(candidate_id=candidate_id)


# E5 - PATCH - withdraw a candidate nomination

@app.patch("/Candidates/{candidate_id}/withdraw")
def withdraw_candidate(candidate_id, roll_no):
    phase = functions.get_current_phase()
    if phase != "nomination":
        raise HTTPException(status_code=400, detail="Nominations are not currently open")
    if roll_no != functions.get_candidate_by_id(candidate_id)["roll_no"]:
        raise HTTPException(status_code=403, detail="You are not authorized to withdraw this candidate")
    candidate = functions.get_candidate_by_id(candidate_id)
    if candidate["status"] != "approved" and candidate["status"] != "nominated":
        raise HTTPException(status_code=400, detail="Candidate is not nominated")
    if candidate["status"] == "withdrawn":
        raise HTTPException(status_code=400, detail="Candidate is already withdrawn")
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return functions.withdraw_candidate(candidate_id=candidate_id, roll_no=roll_no)


# E6 - GET - the current election phase

@app.get("/Election/phase")
def get_election_phase():
    return functions.get_current_phase()


# E7 - PATCH - move to the next election phase

@app.patch("/Election/phase/next")
def move_to_next_phase():
    return functions.move_to_next_phase()



# E8 - POST - cast a vote

@app.post("/Votes")
def cast_vote(voter_roll:str, candidate_id:int):   
    phase = functions.get_current_phase()
    if phase != "voting":
        raise HTTPException(status_code=400, detail="Voting is not currently open")
    candidate = functions.get_candidate_by_id(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")  
    if candidate["status"] != "approved":
        raise HTTPException(status_code=400, detail="Candidate is not approved")
    positions = functions.get_student_votes(voter_roll)
    if candidate["position"] in positions:
        raise HTTPException(status_code=400, detail="You have already voted for this position")
    return functions.cast_vote(voter_roll=voter_roll, candidate_id=candidate_id)


# E9 - GET - get the positions alredy voted by a voter

@app.get("/Votes/{voter_roll}")
def get_positions_voted(voter_roll):
    phase = functions.get_current_phase()
    if phase != "voting":
        raise HTTPException(status_code=400, detail="Voting is not currently open")
    return functions.get_student_votes (roll_no=voter_roll)
                            

# E10 - GET - get the results of the election

@app.get("/Results")
def get_results():
    phase = functions.get_current_phase()
    if phase != "results":
        raise HTTPException(status_code=400, detail="Results are not currently available")  
    return functions.get_results()