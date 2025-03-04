from typing import List, Dict
from .time_manager import TimeManager
from dataclasses import dataclass
from entities.person import Person
from entities.corporation import Corporation
from systems.economy import EconomySystem
from systems.politics import PoliticalSystem

@dataclass
class WorldConfig:
    """Configuration for world initialization"""
    initial_population: int = 1000
    region_count: int = 5
    initial_resources: Dict[str, float] = None
    
    def __post_init__(self):
        if self.initial_resources is None:
            self.initial_resources = {
                "food": 10000.0,
                "water": 20000.0,
                "energy": 15000.0,
                "minerals": 5000.0
            }

class World:
    def __init__(self, config: WorldConfig):
        self.config = config
        self.time = TimeManager()
        self.population: List[Person] = []
        self.corporations: List[Corporation] = []
        self.economy = EconomySystem()
        self.politics = PoliticalSystem()
        self._initialize_world()
        
    def _initialize_world(self):
        """Initialize the world with starting conditions"""
        # Initialize political system first as it affects other systems
        self.politics.initialize_governments(self.config.region_count)
        
        # Initialize corporations
        self.corporations = Corporation.generate_initial_corporations(50)
        
        # Initialize population
        for i in range(self.config.initial_population):
            person = Person(
                person_id=i,
                age=20 + i % 40,  # Ages 20-60
                education_level=i % 5 + 1,  # Levels 1-5
                skills={"general": 0.5},
                wealth=1000.0
            )
            self.population.append(person)
            
        # Initialize economy with resources
        self.economy.initialize_markets(self.config.initial_resources)
        
    def update(self):
        """Update the world state for one time step"""
        try:
            # Update time
            current_year = self.time.current_year
            
            # Update systems
            self.politics.update(current_year)
            self.economy.update(self.corporations, self.population)
            
            # Update entities
            for corporation in self.corporations:
                corporation.produce_resources()
                corporation.calculate_operating_costs()
                corporation.calculate_revenue(self.economy.get_market_prices())
                
            for person in self.population:
                person.update(self.economy)
            
            # Advance time
            self.time.advance_year()
            
            return True
            
        except Exception as e:
            print(f"Error en la simulación: {str(e)}")
            return False
            
    def get_current_year(self) -> int:
        """Get the current year of the simulation"""
        return self.time.current_year
        
    def get_statistics(self) -> Dict:
        """Get current statistics of the world"""
        return {
            "year": self.time.current_year,
            "population": len(self.population),
            "corporations": len(self.corporations),
            "market_prices": self.economy.get_market_prices(),
            "political_state": self.politics.get_state_report(),
            "average_wealth": sum(p.wealth for p in self.population) / len(self.population) if self.population else 0
        } 