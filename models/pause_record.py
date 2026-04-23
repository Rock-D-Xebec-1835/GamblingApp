class PauseRecord:
    def __init__(self, start_time, end_time=None, reason=None):
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return 0