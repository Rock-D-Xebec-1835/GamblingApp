from abc import ABC, abstractmethod
import random

class OutcomeStrategy(ABC):
    @abstractmethod
    def is_win(self):
        pass

class RandomOutcomeStrategy(OutcomeStrategy):
    def __init__(self, probability):
        self.probability = probability
    
    def is_win(self):
        return random.random() < self.probability
    
class WeightedProbabilityStrategy(OutcomeStrategy):
    def __init__(self, probability: float, house_edge: float = 0.05):
        self.base_probability = probability
        self.house_edge = house_edge
    
    def is_win(self):
        adjusted_prob = max(0, self.base_probability - self.house_edge)
        return random.random() < adjusted_prob