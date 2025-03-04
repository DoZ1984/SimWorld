from dataclasses import dataclass
from typing import Dict

@dataclass
class EconomicState:
    resources: Dict[str, float]
    prices: Dict[str, float]
    demand: Dict[str, float]
    supply: Dict[str, float]
    unemployment_rate: float = 0.05

class EconomySystem:
    def __init__(self):
        self.state = EconomicState(
            resources={},
            prices={},
            demand={},
            supply={}
        )
        self.job_market = []
        
    def set_initial_resources(self, resources: Dict[str, float]):
        self.state.resources = resources
        # Establecer precios iniciales basados en recursos
        self.state.prices = {
            resource: 100.0 / (quantity + 1e-5)  # Evitar división por cero
            for resource, quantity in resources.items()
        }
        
    def update(self, world):
        # Actualizar oferta y demanda
        self._calculate_demand(world)
        self._calculate_supply()
        self._adjust_prices()
        
        # Actualizar mercado laboral
        self._update_job_market(world)
    
    def _calculate_demand(self, world):
        # Calcular demanda basada en población
        total_pop = len(world.population)
        self.state.demand = {
            'food': total_pop * 0.8,
            'water': total_pop * 1.2,
            'energy': total_pop * 0.5
        }
    
    def _calculate_supply(self):
        # Calcular oferta basada en recursos
        self.state.supply = {
            resource: quantity * 0.8  # Eficiencia de producción
            for resource, quantity in self.state.resources.items()
        }
    
    def _adjust_prices(self):
        # Ajustar precios basados en oferta/demanda
        for resource in self.state.prices:
            demand = self.state.demand.get(resource, 0)
            supply = self.state.supply.get(resource, 0)
            ratio = demand / (supply + 1e-5)
            self.state.prices[resource] *= 1 + (ratio - 1) * 0.1  # Factor de ajuste
            
    def _update_job_market(self, world):
        # Actualizar ofertas de empleo
        self.job_market = [
            job for corp in world.corporations
            for job in corp.generate_job_openings()
        ]
        # Calcular tasa de desempleo
        employed = sum(1 for p in world.population if p.job)
        self.state.unemployment_rate = 1 - (employed / len(world.population)) 