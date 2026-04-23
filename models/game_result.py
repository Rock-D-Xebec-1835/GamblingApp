
class GameResult:
    def __init__(self, result, amount, odds, profit, balance_after):
        self.result = result
        self.amount = amount
        self.odds = odds
        self.profit = profit
        self.balance_after = balance_after

    def __str__(self):
        return f"{self.result} | Bet: {self.amount} | Profit: {self.profit} | Balance: {self.balance_after}"