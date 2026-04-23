class Bet:
    def __init__(self, bet_id=None, gambler_id=None, session_id=None, amount=0.0, result=None, stake_before=None, stake_after=None, odds=None, created_at=None):
        self.bet_id = bet_id
        self.gambler_id = gambler_id
        self.session_id = session_id
        self.amount = amount
        self.result = result
        self.stake_before = stake_before
        self.stake_after = stake_after
        self.created_at = created_at
        self.odds = odds