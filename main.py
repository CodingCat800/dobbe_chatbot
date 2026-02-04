from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from sql import get_connection



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/")
def health():
    return {"status": "running"}

@app.get("/appointments/{doctor_id}")
def get_appointments(doctor_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT patient_name, date, time
        FROM appointments
        WHERE doctor_id = %s
        ORDER BY date, time
        """,
        (doctor_id,),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "patient": r[0],
            "date": str(r[1]),
            "time": r[2].strftime("%I:%M %p").lstrip("0"),
        }
        for r in rows
    ]

@app.post("/chat")
async def chat(req: ChatRequest):
    response = await run_agent(
        session_id=req.session_id,
        user_message=req.message
    )
    return {"response": response}
