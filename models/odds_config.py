class OddsConfig:
    def __init__(self, odds_type=None):
        self.odds_type = odds_type

    def calculate_odds(self, probability):
        if self.odds_type == "FIXED":
            return 2.0
        elif self.odds_type == "PROBABILITY":
            return round(1/probability,2)
        elif self.odds_type == "DECIMAL":
            return round(1/probability,2)
        elif self.odds_type == "AMERICAN":
            if probability >= 0.5:
                return round(-(probability/(1-probability)) * 100)
            else:
                return round((1-probability)/probability * 100)
        else:
            raise ValueError("Unsupported odds type")