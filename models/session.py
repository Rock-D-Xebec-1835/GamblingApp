
class Session:
    def __init__(self, session_id=None, gambler_id=None, start_time=None, end_time=None, status="ACTIVE", end_reason=None):
        self.session_id = session_id
        self.gambler_id = gambler_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.end_reason = end_reason