from dataclasses import dataclass, field
from typing import List, Dict
import random
from enum import Enum

class PersonalityType(Enum):
    NEUROTIC = "Neurotic"
    CONSCIENTIOUS = "Conscientious"
    OPEN = "Open"
    AGREEABLE = "Agreeable"
    EXTROVERT = "Extrovert"

@dataclass
class Skill:
    name: str
    level: float
    experience: float = 0.0

@dataclass
class Relationship:
    target_id: int
    type: str  # 'friend', 'family', 'romantic', etc.
    strength: float

@dataclass
class Person:
    """Represents an individual in the simulation"""
    person_id: int
    age: int
    education_level: int  # 1-5 scale (1: Basic, 5: PhD)
    skills: Dict[str, float] = field(default_factory=dict)  # skill_name -> proficiency (0.0-1.0)
    wealth: float = 0.0
    salary: float = 0.0
    employer_id: int = -1  # -1 means unemployed
    happiness: float = 0.5  # 0.0-1.0 scale
    health: float = 1.0  # 0.0-1.0 scale
    location: int = 0  # region_id
    
    def update(self, economy):
        """Update person's state for one time step"""
        # Age the person
        self.age += 1
        
        # Basic needs consumption
        basic_needs_cost = 1000  # Monthly basic needs cost
        if self.wealth >= basic_needs_cost:
            self.wealth -= basic_needs_cost
            self.happiness = min(1.0, self.happiness + 0.1)
        else:
            self.happiness = max(0.0, self.happiness - 0.2)
            self.health = max(0.0, self.health - 0.1)
        
        # Income from salary
        if self.employer_id != -1:
            self.wealth += self.salary
            
        # Random life events
        self._handle_random_events()
        
        # Update skills through experience
        if self.employer_id != -1:
            for skill in self.skills:
                if self.skills[skill] < 1.0:
                    self.skills[skill] = min(1.0, self.skills[skill] + 0.01)
    
    def _handle_random_events(self):
        """Handle random life events that affect the person"""
        # Small random fluctuations in happiness and health
        self.happiness += random.uniform(-0.05, 0.05)
        self.happiness = max(0.0, min(1.0, self.happiness))
        
        self.health += random.uniform(-0.02, 0.02)
        self.health = max(0.0, min(1.0, self.health))
    
    def get_employability(self) -> float:
        """Calculate person's employability score"""
        education_factor = self.education_level / 5.0
        skills_factor = sum(self.skills.values()) / max(len(self.skills), 1)
        health_factor = self.health
        
        return (education_factor * 0.4 + skills_factor * 0.4 + health_factor * 0.2)
    
    def apply_for_job(self, job_opening: Dict) -> bool:
        """Attempt to apply for a job opening"""
        if self.employer_id != -1:
            return False  # Already employed
            
        # Check if person meets basic requirements
        if (self.education_level >= job_opening["requirements"]["education_level"] and
            self.get_employability() > 0.5):
            return True
            
        return False
    
    def get_status(self) -> Dict:
        """Get current status of the person"""
        return {
            "id": self.person_id,
            "age": self.age,
            "education": self.education_level,
            "wealth": self.wealth,
            "employed": self.employer_id != -1,
            "happiness": self.happiness,
            "health": self.health,
            "skills": self.skills
        }

    def __post_init__(self):
        self.name: str = ""
        self.health: float = 100.0
        self.intelligence: float = random.uniform(70, 130)
        self.personality: PersonalityType = random.choice(list(PersonalityType))
        self.relationships: List[Relationship] = []
        self.needs = {
            'hunger': 0.0,
            'energy': 100.0,
            'happiness': 75.0
        }
        self.job = None
        self.finances = {
            'cash': 1000.0,
            'salary': 0.0,
            'savings': 0.0,
            'taxes_paid': 0.0
        }
        self.employment_status = "unemployed"
        self.skills = {
            'farming': Skill(name='farming', level=random.normalvariate(50, 15)),
            'manufacturing': Skill(name='manufacturing', level=random.normalvariate(50, 15))
        }
        self.region = None  # Nueva propiedad para el sistema regional
    
    @classmethod
    def generate_random(cls):
        person = cls()
        person.age = random.randint(18, 90)
        person.name = "Nombre Generado"  # Implementar generador de nombres
        return person
    
    def _make_decisions(self, world):
        # Implementar lógica compleja de comportamiento
        if self.needs['hunger'] > 70:
            self._satisfy_hunger()
        
        if self.finances['cash'] < 100:
            self._find_job(world)
    
    def _satisfy_hunger(self):
        # Implementar lógica para comer
        pass
    
    def _find_job(self, world):
        # Buscar trabajo en el mercado laboral
        for job in world.economy.job_market:
            if self._meets_job_requirements(job):
                self._accept_job(job)
                break
                
    def _meets_job_requirements(self, job):
        return self.skills[job.required_skill].level >= job.required_level
        
    def _accept_job(self, job):
        self.job = job
        self.employment_status = "employed"
        self.finances['salary'] = job.salary 
    
    def _handle_finances(self, world):
        """Gestiona las finanzas personales incluyendo impuestos"""
        if self.job:
            # Recibir salario
            gross_salary = self.finances['salary']
            tax = world.economy.tax_system.calculate_tax(gross_salary)
            net_salary = gross_salary - tax
            
            self.finances['cash'] += net_salary
            self.finances['taxes_paid'] += tax
            
            # Gestionar ahorros
            if self.finances['cash'] > gross_salary * 2:
                savings = self.finances['cash'] * 0.1
                self.finances['cash'] -= savings
                self.finances['savings'] += savings 