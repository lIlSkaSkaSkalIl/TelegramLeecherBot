# handlers/state_manager.py

USER_STATE = {}  # format: {chat_id: {"mode": "gd", "step": "awaiting_link"}}

def set_state(chat_id: int, mode: str, step: str = "awaiting_link"):
    USER_STATE[chat_id] = {"mode": mode, "step": step}

def get_state(chat_id: int):
    return USER_STATE.get(chat_id)

def clear_state(chat_id: int):
    if chat_id in USER_STATE:
        del USER_STATE[chat_id]
