class Bet:
    def __init__(self, bet_id=None, gambler_id=None, session_id=None, amount=0.0, result=None, created_at=None):
        self.bet_id = bet_id
        self.gambler_id = gambler_id
        self.session_id = session_id
        self.amount = amount
        self.result = result
        self.created_at = created_at