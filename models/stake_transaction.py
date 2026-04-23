class StakeTransaction:
    def __init__(self, txn_id=None, gambler_id=None, session_id=None, type=None, amount=0.0, balance_after=0.0, created_at=None):
        self.txn_id = txn_id
        self.gambler_id = gambler_id
        self.session_id = session_id
        self.type = type
        self.amount = amount
        self.balance_after = balance_after
        self.created_at = created_at