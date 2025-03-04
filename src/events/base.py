from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability
        
    @abstractmethod
    def trigger(self, world):
        pass

class EconomicEvent(Event):
    TYPE = "economic" 