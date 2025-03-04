from dataclasses import dataclass
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

class Person:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.age: int = 0
        self.health: float = 100.0
        self.intelligence: float = random.uniform(70, 130)
        self.personality: PersonalityType = random.choice(list(PersonalityType))
        self.skills: Dict[str, Skill] = {}
        self.relationships: List[Relationship] = []
        self.needs = {
            'hunger': 0.0,
            'energy': 100.0,
            'happiness': 75.0
        }
        self.job = None
        self.finances = {
            'cash': 0.0,
            'debt': 0.0,
            'salary': 0.0
        }
        self.employment_status = "unemployed"
        self.skills = {
            'farming': Skill(name='farming', level=random.normalvariate(50, 15)),
            'manufacturing': Skill(name='manufacturing', level=random.normalvariate(50, 15))
        }
    
    @classmethod
    def generate_random(cls):
        person = cls()
        person.age = random.randint(18, 90)
        person.name = "Nombre Generado"  # Implementar generador de nombres
        return person
    
    def update(self, world):
        # Actualizar necesidades básicas
        self.needs['hunger'] = min(self.needs['hunger'] + 0.1, 100)
        self.needs['energy'] = max(self.needs['energy'] - 0.5, 0)
        
        # Lógica de toma de decisiones
        self._make_decisions(world)
    
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