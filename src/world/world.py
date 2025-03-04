from dataclasses import dataclass
from typing import Dict, List
from .time_manager import TimeManager
from entities.person import Person
from entities.corporation import Corporation
from systems.economy import EconomySystem
from systems.politics import PoliticalSystem

@dataclass
class WorldConfig:
    population_size: int = 1000
    start_year: int = 2024
    region_count: int = 10
    initial_resources: Dict[str, float] = None

class World:
    def __init__(self, config: WorldConfig):
        self.config = config
        self.time_manager = TimeManager(start_year=config.start_year)
        self.population: List[Person] = []
        self.corporations: List[Corporation] = []
        self.economy = EconomySystem()
        self.politics = PoliticalSystem()
        self._initialize_world()
        
    def _initialize_world(self):
        # Generar población inicial
        self.population = [Person.generate_random() for _ in range(self.config.population_size)]
        
        # Crear gobiernos y corporaciones iniciales
        self.politics.initialize_governments(self.config.region_count)
        self.corporations = Corporation.generate_initial_corporations(50)
        
        # Configurar recursos iniciales
        if self.config.initial_resources:
            self.economy.set_initial_resources(self.config.initial_resources)
    
    def run(self, years: int = 1):
        """Avanza la simulación X años"""
        for _ in range(years):
            self._run_year_cycle()
    
    def _run_year_cycle(self):
        self.time_manager.advance_year()
        
        # Actualizar todos los sistemas
        self.economy.update(self)
        self.politics.update(self)
        
        # Actualizar entidades
        for person in self.population:
            person.update(self)
            
        for corp in self.corporations:
            corp.update(self)
            
        # Procesar eventos globales
        self._process_world_events()
    
    def _process_world_events(self):
        # Lógica para manejar eventos globales
        pass 