class SessionStatistics:
    def __init__(self):
        self.total_bets = 0
        self.wins = 0
        self.losses = 0
        self.net_profit = 0.0
        self.current_streak = 0
        self.max_streak = 0
        self.largest_win = 0
        self.largest_loss = 0
        self.total_win_amount = 0
        self.total_lose_amount = 0

    def record(self, result, amount):
        self.total_bets += 1

        if result == "WIN":
            self.wins += 1
            self.net_profit += amount
            self.current_streak = max(1, self.current_streak + 1)
            self.total_win_amount += amount
            self.largest_win = max(self.largest_win,amount)
        else:
            self.losses += 1
            self.net_profit -= amount
            self.current_streak = min(-1, self.current_streak + 1)
            self.total_lose_amount += amount
            self.largest_loss = max(self.largest_loss, amount)
        
        self.max_streak = max(self.max_streak, abs(self.current_streak))
    
    def win_rate(self):
        if self.total_bets == 0:
            return 0
        return(self.wins / self.total_bets) * 100
    
    def profit_factor(self):
        if self.total_lose_amount == 0:
            return float('inf')
        return self.total_win_amount / self.total_lose_amount