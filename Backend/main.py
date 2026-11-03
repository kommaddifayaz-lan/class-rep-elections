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

# E1 - get candidates with position and approved people only

@app.get("/candidates")
def get_candidates(position: str = None, approved_only: bool = False):
    allowed_positions = ["class_rep","sports_secretary","cultural_secretary","teach_secretary"]
    if position is not None and position not in allowed_positions:
        raise HTTPException(status_code=400, detail="Invalid position")
    return function.get_all_candidates(position=position, approved_only=approved_only)

# E2 - get candidate by id

@app.get("/candidates/{candidate_id}") 
def get_candidate(candidate_id: int):
    candidate = function.get_candidate_by_id(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

# E3 - 