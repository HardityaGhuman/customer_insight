import json
import os
from datetime import datetime

STATE_DIR = "state"
STATE_FILE = os.path.join(STATE_DIR, "system_state.json")

DEFAULT_STATE = {
    "issue_counts": {
        "billing": 0,
        "delivery": 0,
        "product": 0,
        "support": 0,
        "app": 0,
        "other": 0
    },
    "escalation": {
        "has_been_escalated": False,
        "level": "none"
    },
    "last_updated": None
}


def load_state():
    if not os.path.exists(STATE_FILE):
        return DEFAULT_STATE.copy()

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)

    state["last_updated"] = datetime.utcnow().isoformat()

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)