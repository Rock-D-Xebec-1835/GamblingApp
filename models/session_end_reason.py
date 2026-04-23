from enum import Enum

class SessionEndReason(Enum):
    WIN_LIMIT = "WIN_LIMIT"
    LOSS_LIMIT = "LOSS_LIMIT"
    MANUAL = "MANUAL"
    TIMEOUT = "TIMEOUT"

    