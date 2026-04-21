
class Gambler:
    def __init__(self, gambler_id=None, name=None, initial_balance=0.0, current_balance=0.0, total_winnings=0.0, total_bets=0, min_balance=0.0, win_threshold=0.0, loss_threshold=0.0, created_at=None):
        self.gambler_id = gambler_id
        self.name = name
        self.initial_balance = initial_balance
        self.current_balance = current_balance
        self.total_winnings = total_winnings
        self.total_bets = total_bets
        self.min_balance = min_balance
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.created_at = created_at
