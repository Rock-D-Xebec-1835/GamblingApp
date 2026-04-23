from abc import ABC, abstractmethod

class BettingStrategy(ABC):
    @abstractmethod
    def next_bet(self, gambler):
        pass

    @abstractmethod
    def record_result(self, result):
        pass