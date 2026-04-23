import time
class Session:
    def __init__(self, session_id=None, gambler_id=None, start_time=None, end_time=None, status="INITIALIZED", end_reason=None, pause_records=[], paused_at=None, total_pause_time=0):
        self.session_id = session_id
        self.gambler_id = gambler_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.end_reason = end_reason
        self.pause_records = pause_records
        self.paused_at = paused_at
        self.total_pause_time = total_pause_time

