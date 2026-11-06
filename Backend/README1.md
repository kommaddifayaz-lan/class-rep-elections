Problem Statement:

Student council elections are usually run on paper slips or WhatsApp polls. Nominations get lost, anyone can vote more than once, and the results can leak before the election ends. A class needs one place where students nominate themselves, an officer approves the nominations, each student votes once per position, and nobody sees the results until the election is closed.   

We are building an election app where students nominate, the officer approves, everyone votes once per position, and the results stay hidden until the election is closed.

contributions:

praneeth - designed the DB and backend functions(E2,E4,E5,E6).

siva - backend functions(E1,E3,E7,E8,E9,E10)

fayaz - main.py(10 Endpoints)

Progess:

First we designed the database using SQLite, then we developed the backend using FastAPI. we didn't completed the frontend.

Demo--

Code file structure:

class-rep-elections/                                                                                                                                                                                                                               

├── backend/

│   ├── Elections.db  -- stores candidates, votes and elections information.

│   ├── functions.py -- Database operations and backend functions.

│   └── main.py -- FastAPI application and API endpoints.

└── README.md

Bugs:

1. Merge issue
   <img width="962" height="426" alt="image" src="https://github.com/user-attachments/assets/668bb0bd-a085-41bf-953e-f3eaab8ca2d7" />

2. venv activate
   <img width="792" height="77" alt="image" src="https://github.com/user-attachments/assets/f4d5d3b5-a77c-470e-87a0-908afa4d0274" />



3. module: attribute


   <img width="302" height="114" alt="image" src="https://github.com/user-attachments/assets/39662513-2773-48c7-8013-863c396f5f3c" />

 

