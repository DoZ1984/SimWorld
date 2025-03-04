from typing import Dict, List
from dataclasses import dataclass, field
import random

def generate_company_name() -> str:
    """Generate a random but plausible company name"""
    prefixes = ["Global", "Advanced", "United", "International", "Strategic", "Dynamic", "Premier", "Elite"]
    core_names = ["Tech", "Industries", "Solutions", "Resources", "Energy", "Materials", "Systems", "Enterprises"]
    suffixes = ["Corp", "Inc", "Ltd", "Group", "Holdings", "International", "Co", "Corporation"]
    
    return f"{random.choice(prefixes)} {random.choice(core_names)} {random.choice(suffixes)}"

@dataclass
class Corporation:
    """
    Represents a business entity in the simulation that can produce goods,
    hire workers, and participate in the market.
    """
    id: int
    name: str
    industry_type: str  # e.g., "manufacturing", "agriculture", "services"
    capital: float = 1000000.0  # Initial capital
    employees: List[int] = field(default_factory=list)  # List of employee IDs
    inventory: Dict[str, float] = field(default_factory=dict)  # Resource -> quantity
    production_capacity: Dict[str, float] = field(default_factory=dict)  # Resource -> production rate
    operating_costs: float = 0.0
    revenue: float = 0.0
    profit_margin: float = 0.15  # 15% default profit margin
    
    @staticmethod
    def generate_initial_corporations(count: int) -> List['Corporation']:
        """Generate a list of initial corporations with random but realistic attributes"""
        corporations = []
        industry_types = ["manufacturing", "agriculture", "services", "technology", "energy", "mining"]
        
        # Resource types and their base production rates
        resource_production_rates = {
            "food": (100, 500),
            "water": (200, 1000),
            "energy": (500, 2000),
            "minerals": (50, 200),
            "consumer_goods": (100, 400),
            "industrial_goods": (50, 200)
        }

        for i in range(count):
            # Select random industry type
            industry = random.choice(industry_types)
            
            # Generate initial production capacities based on industry
            production_capacity = {}
            if industry == "agriculture":
                production_capacity["food"] = random.uniform(*resource_production_rates["food"])
            elif industry == "manufacturing":
                production_capacity["consumer_goods"] = random.uniform(*resource_production_rates["consumer_goods"])
                production_capacity["industrial_goods"] = random.uniform(*resource_production_rates["industrial_goods"])
            elif industry == "energy":
                production_capacity["energy"] = random.uniform(*resource_production_rates["energy"])
            elif industry == "mining":
                production_capacity["minerals"] = random.uniform(*resource_production_rates["minerals"])
            
            # Create corporation with random initial values
            corporation = Corporation(
                id=i,
                name=generate_company_name(),
                industry_type=industry,
                capital=random.uniform(500000, 5000000),
                production_capacity=production_capacity,
                profit_margin=random.uniform(0.10, 0.25)
            )
            
            # Initialize inventory with some starting resources
            for resource, rate in corporation.production_capacity.items():
                corporation.inventory[resource] = rate * random.uniform(0.5, 2.0)
            
            corporations.append(corporation)
        
        return corporations
    
    def hire_employee(self, person_id: int) -> bool:
        """Add an employee to the corporation"""
        if person_id not in self.employees:
            self.employees.append(person_id)
            return True
        return False
    
    def fire_employee(self, person_id: int) -> bool:
        """Remove an employee from the corporation"""
        if person_id in self.employees:
            self.employees.remove(person_id)
            return True
        return False
    
    def update_inventory(self, resource: str, quantity: float):
        """Update the quantity of a resource in inventory"""
        self.inventory[resource] = self.inventory.get(resource, 0) + quantity
        
    def produce_resources(self):
        """Produce resources based on production capacity"""
        for resource, rate in self.production_capacity.items():
            produced_amount = rate * len(self.employees)  # Production based on workforce
            self.update_inventory(resource, produced_amount)
            
    def calculate_operating_costs(self):
        """Calculate monthly operating costs"""
        # Basic implementation - can be expanded based on various factors
        employee_costs = len(self.employees) * 5000  # Average monthly salary
        maintenance_costs = sum(self.production_capacity.values()) * 100
        self.operating_costs = employee_costs + maintenance_costs
        
    def calculate_revenue(self, market_prices: Dict[str, float]):
        """Calculate monthly revenue based on sales and market prices"""
        self.revenue = sum(
            quantity * market_prices.get(resource, 0)
            for resource, quantity in self.inventory.items()
        )
        
    def get_financial_status(self) -> Dict[str, float]:
        """Return the current financial status of the corporation"""
        return {
            "capital": self.capital,
            "revenue": self.revenue,
            "operating_costs": self.operating_costs,
            "profit": self.revenue - self.operating_costs
        }
        
    def generate_job_openings(self) -> List[Dict]:
        """Generate job openings based on corporation needs and growth"""
        job_openings = []
        
        # Base number of desired employees based on production capacity
        total_production_rate = sum(self.production_capacity.values())
        desired_employees = max(5, int(total_production_rate / 100))  # At least 5 employees
        
        # Calculate how many positions to open
        current_employees = len(self.employees)
        openings_count = max(0, desired_employees - current_employees)
        
        # Generate job positions based on industry type
        job_types = {
            "manufacturing": ["Production Worker", "Quality Control", "Plant Manager"],
            "agriculture": ["Farm Worker", "Agricultural Technician", "Field Manager"],
            "services": ["Service Representative", "Account Manager", "Operations Coordinator"],
            "technology": ["Software Developer", "System Administrator", "IT Specialist"],
            "energy": ["Plant Operator", "Maintenance Technician", "Energy Engineer"],
            "mining": ["Mining Operator", "Safety Inspector", "Site Manager"]
        }
        
        base_salaries = {
            "Worker": (30000, 45000),
            "Technician": (40000, 60000),
            "Manager": (60000, 100000),
            "Specialist": (50000, 80000),
            "Engineer": (70000, 110000)
        }
        
        available_positions = job_types.get(self.industry_type, ["General Worker"])
        
        for _ in range(openings_count):
            position = random.choice(available_positions)
            
            # Determine salary range based on position level
            if "Manager" in position:
                salary_range = base_salaries["Manager"]
            elif "Engineer" in position or "Developer" in position:
                salary_range = base_salaries["Engineer"]
            elif "Technician" in position or "Specialist" in position:
                salary_range = base_salaries["Specialist"]
            else:
                salary_range = base_salaries["Worker"]
                
            job_opening = {
                "corporation_id": self.id,
                "corporation_name": self.name,
                "position": position,
                "industry": self.industry_type,
                "salary": random.uniform(*salary_range),
                "requirements": {
                    "education_level": random.randint(1, 5),  # 1: Basic, 5: PhD
                    "experience_years": random.randint(0, 10)
                }
            }
            
            job_openings.append(job_opening)
            
        return job_openings 