
class SessionSummary:

    @staticmethod
    def display(stats):
        print("\n=== SESSION SUMMARY ===")
        print(f"Total Bets: {stats.total_bets}")
        print(f"Wins: {stats.wins}")
        print(f"Losses: {stats.losses}")
        print(f"Win Rate: {stats.win_rate():.2f}%")
        print(f"Net Profit: {stats.net_profit}")
        print(f"Max Streak: {stats.max_streak}")