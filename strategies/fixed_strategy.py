from strategies.base_strategy import BettingStrategy

class FixedAmountStrategy(BettingStrategy):
    def __init__(self, amount):
        self.amount = amount

    def next_bet(self, gambler):
        return self.amount
    
    def record_result(self, result):
        pass