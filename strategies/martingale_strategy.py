from strategies.base_strategy import BettingStrategy

class MartingaleStrategy(BettingStrategy):
    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.current_bet = base_amount

    def next_bet(self, gambler):
        return self.current_bet
    
    def record_result(self, result):
        if result == "LOSS":
            self.current_bet *= 2
        else:
            self.current_bet = self.base_amount