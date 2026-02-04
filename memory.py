SESSION_MEMORY = {}

def get_session(session_id: str):
    return SESSION_MEMORY.get(session_id, [])

def update_session(session_id: str, messages):
    SESSION_MEMORY[session_id] = messages