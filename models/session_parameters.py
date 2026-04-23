class SessionParameters:
    def __init__(self,
                win_threshold,
                loss_threshold,
                min_bet=10,
                max_bet=1000,
                max_games=100,
                max_duration=300,
                win_probability=None
                ):
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.max_games = max_games
        self.max_duration = max_duration
        self.win_probability = win_probability
