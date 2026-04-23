class StakeBoundary:
    def __init__(self, win_threshold, loss_threshold):
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold

        self.win_warning = win_threshold * 0.8
        self.loss_warning = loss_threshold * 1.2

    def check_warning(self, balance):
        if balance >= self.win_warning and balance < self.win_threshold:
            return "WIN_WARNING"
        if balance <= self.loss_warning and balance > self.loss_threshold:
            return "LOSS_WARNING"
        return None
    
    def check_limit(self, balance):
        if balance >= self.win_threshold:
            return "WIN_LIMIT"
        if balance <= self.loss_threshold:
            return "LOSS_LIMIT"
        return None
    
