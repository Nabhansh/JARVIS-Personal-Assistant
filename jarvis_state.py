from jarvis_state import set_state

HUD_STATE = "IDLE"
HUD_COMMAND = ""

def set_state(state, command=""):
    global HUD_STATE, HUD_COMMAND
    HUD_STATE = state
    HUD_COMMAND = command

def get_state():
    return HUD_STATE, HUD_COMMAND