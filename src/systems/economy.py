from dataclasses import dataclass
from typing import Dict, List
from enum import Enum
from entities.corporation import Corporation
from entities.person import Person

@dataclass
class EconomicState:
    resources: Dict[str, float]
    prices: Dict[str, float]
    demand: Dict[str, float]
    supply: Dict[str, float]
    unemployment_rate: float = 0.05

class TaxBracket:
    def __init__(self, min_income: float, max_income: float, rate: float):
        self.min_income = min_income
        self.max_income = max_income
        self.rate = rate

class TaxSystem:
    def __init__(self):
        self.brackets = [
            TaxBracket(0, 10000, 0.10),        # 10% hasta 10k
            TaxBracket(10001, 30000, 0.20),    # 20% 10k-30k
            TaxBracket(30001, 70000, 0.30),    # 30% 30k-70k
            TaxBracket(70001, float('inf'), 0.35)  # 35% más de 70k
        ]
        self.total_revenue = 0.0

    def calculate_tax(self, income: float) -> float:
        total_tax = 0.0
        remaining_income = income

        for bracket in self.brackets:
            if remaining_income <= 0:
                break

            taxable_amount = min(
                remaining_income,
                bracket.max_income - bracket.min_income
            )
            tax = taxable_amount * bracket.rate
            total_tax += tax
            remaining_income -= taxable_amount

        return total_tax

class EconomySystem:
    def __init__(self):
        self.state = EconomicState(
            resources={},
            prices={},
            demand={},
            supply={}
        )
        self.job_market = []
        self.tax_system = TaxSystem()
        self.regional_markets = {}
        self.markets: Dict[str, float] = {}
        
    def set_initial_resources(self, resources: Dict[str, float]):
        self.state.resources = resources
        # Establecer precios iniciales basados en recursos
        self.state.prices = {
            resource: 100.0 / (quantity + 1e-5)  # Evitar división por cero
            for resource, quantity in resources.items()
        }
        
    def initialize_markets(self, initial_resources: Dict[str, float]):
        """Initialize the markets with given resources"""
        self.markets = initial_resources.copy()
        
    def update(self, corporations: List[Corporation], population: List[Person]):
        # Actualizar oferta y demanda
        self._calculate_demand(population)
        self._calculate_supply(corporations)
        self._adjust_prices()
        
        # Actualizar mercado laboral y recaudar impuestos
        self._update_job_market(corporations, population)
        self._collect_taxes(population)
        
        # Actualizar flujos económicos regionales
        self._update_regional_markets()
    
    def _calculate_demand(self, population: List[Person]):
        # Calcular demanda basada en población
        total_pop = len(population)
        self.state.demand = {
            'food': total_pop * 0.8,
            'water': total_pop * 1.2,
            'energy': total_pop * 0.5
        }
    
    def _calculate_supply(self, corporations: List[Corporation]):
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
            
    def _update_job_market(self, corporations: List[Corporation], population: List[Person]):
        # Actualizar ofertas de empleo
        self.job_market = [
            job for corp in corporations
            for job in corp.generate_job_openings()
        ]
        # Calcular tasa de desempleo
        employed = sum(1 for p in population if p.job)
        self.state.unemployment_rate = 1 - (employed / len(population)) 
    
    def _collect_taxes(self, population: List[Person]):
        """Recauda impuestos de la población activa"""
        total_revenue = 0.0
        for person in population:
            if person.job and person.finances['salary'] > 0:
                tax = self.tax_system.calculate_tax(person.finances['salary'])
                person.finances['cash'] -= tax
                total_revenue += tax
        self.tax_system.total_revenue = total_revenue
    
    def _update_regional_markets(self):
        """Actualiza los mercados regionales y sus interacciones"""
        for region, market in self.regional_markets.items():
            # Actualizar precios regionales
            for resource, base_price in self.state.prices.items():
                market['prices'][resource] = base_price * market['demand_factor']
            
            # Calcular flujos comerciales entre regiones
            self._calculate_trade_flows(region)
    
    def _calculate_trade_flows(self, region):
        """Calcula flujos comerciales entre regiones basados en diferencias de precios"""
        for other_region, other_market in self.regional_markets.items():
            if region != other_region:
                for resource in self.state.prices:
                    price_diff = (self.regional_markets[region]['prices'][resource] - 
                                other_market['prices'][resource])
                    if abs(price_diff) > 0.1:  # Umbral mínimo para comercio
                        self._execute_trade(region, other_region, resource, price_diff) 

    def get_market_prices(self) -> Dict[str, float]:
        """Get current market prices"""
        return self.markets.copy() 