from strategies.base_strategy import BettingStrategy

class PercentageStrategy(BettingStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def next_bet(self, gambler):
        return gambler.current_balance * self.percentage
    
    def record_result(self, result):
        pass