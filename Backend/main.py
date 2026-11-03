from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions 

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


@app.get("/candidates")
def get_candidates(position: str =None, approved_only: bool = False):
    allowed_positions = ["class_rep","sports_secretary","cultural_secretary","teach_secretary"]
    if position not in allowed_positions:
        raise HTTPException(status_code=400, detail="Invalid position")
    return functions.get_all_candidates()