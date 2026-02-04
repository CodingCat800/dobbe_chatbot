# 🩺 Doctor Appointment & Reporting Assistant

An AI-powered assistant that supports **patient appointment booking** and **doctor reporting** using a single agentic backend.  
The system uses an LLM to infer intent and invoke deterministic tools for scheduling, reporting, and notifications.

---

## ✨ Features

**Patient**
- Check doctor availability
- Book appointments
- Google Calendar scheduling
- Email and WhatsApp confirmations

**Doctor**
- View upcoming appointments (in-app)
- Appointment statistics and summaries

---


## 🏗️ Tech Stack

- Backend: FastAPI
- LLM: Groq (LangChain)
- Database: PostgreSQL
- Frontend: React (Vite)
- Integrations: Google Calendar (OAuth), Email, WhatsApp (Twilio)

---

## 📁 Repository Structure

```text
backend/
├── main.py
├── agent.py
├── tools.py
├── external/
└── requirements.txt

frontend/
└── src/
    ├── App.jsx
    ├── Chat.jsx
    └── Appointments.jsx
```

--- 

## ⚠️ Frontend Note (Important)

Only the src/ folder of the React frontend is included in this repository.
node_modules/ and build files are intentionally excluded.

To run the frontend, a Vite React project must be created and the provided src/ folder replaced.

---

## 🌐 Routes

- / → Chat interface (patient)
- /appointments → Doctor in-app appointments view

---

## 🧠 Design Notes

- A single LLM agent handles multiple user scenarios
- The LLM decides which tool to invoke
- Tool outputs are treated as ground truth
- Doctor in-app notifications are derived directly from appointment data


