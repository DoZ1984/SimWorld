from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random

class GovernmentType(Enum):
    DEMOCRACY = "Democracy"
    AUTOCRACY = "Autocracy"
    OLIGARCHY = "Oligarchy"
    ANARCHY = "Anarchy"

class PolicyArea(Enum):
    TAXATION = "Taxation"
    WELFARE = "Welfare"
    EDUCATION = "Education"
    HEALTHCARE = "Healthcare"
    DEFENSE = "Defense"
    INFRASTRUCTURE = "Infrastructure"

@dataclass
class Policy:
    """Represents a government policy"""
    name: str
    area: PolicyArea
    effect_strength: float  # -1.0 to 1.0
    implementation_cost: float
    public_approval: float = 0.0  # -1.0 to 1.0

@dataclass
class PoliticalParty:
    """Represents a political party"""
    name: str
    ideology: str
    support_level: float = 0.0  # 0.0 to 1.0
    policies: List[Policy] = field(default_factory=list)

@dataclass
class RegionalGovernment:
    """Represents a regional government entity"""
    region_id: int
    government_type: GovernmentType
    local_policies: List[Policy] = field(default_factory=list)
    local_approval: float = 0.5
    autonomy_level: float = 0.5  # How independent from central government (0.0 to 1.0)
    budget: float = 1000000.0
    tax_rate: float = 0.2

class PoliticalSystem:
    """Manages the political aspects of the simulation"""
    def __init__(self):
        self.government_type: GovernmentType = GovernmentType.DEMOCRACY
        self.stability: float = 1.0  # 0.0 to 1.0
        self.parties: List[PoliticalParty] = []
        self.active_policies: List[Policy] = []
        self.public_approval: float = 0.5  # 0.0 to 1.0
        self.corruption_level: float = 0.0  # 0.0 to 1.0
        self.election_cycle: int = 4  # Years between elections
        self.current_ruling_party: Optional[PoliticalParty] = None
        self.regional_governments: Dict[int, RegionalGovernment] = {}
        
    def add_party(self, party: PoliticalParty):
        """Add a new political party to the system"""
        self.parties.append(party)
        
    def implement_policy(self, policy: Policy):
        """Implement a new government policy"""
        self.active_policies.append(policy)
        self.public_approval += policy.public_approval * 0.1
        self.public_approval = max(0.0, min(1.0, self.public_approval))
        
    def hold_election(self) -> Optional[PoliticalParty]:
        """Simulate an election and return the winning party"""
        if not self.parties:
            return None
            
        # Simple election simulation based on party support levels
        winner = max(self.parties, key=lambda p: p.support_level)
        self.current_ruling_party = winner
        return winner
        
    def update_stability(self):
        """Update the political stability based on various factors"""
        # Factors affecting stability:
        # - Public approval
        # - Corruption level
        # - Active policies effectiveness
        stability_factor = (
            self.public_approval * 0.4 +
            (1 - self.corruption_level) * 0.4 +
            (sum(p.effect_strength for p in self.active_policies) / 
             max(len(self.active_policies), 1)) * 0.2
        )
        
        self.stability = max(0.0, min(1.0, stability_factor))
        
    def get_state_report(self) -> Dict:
        """Generate a report of the current political state"""
        return {
            "government_type": self.government_type.value,
            "stability": self.stability,
            "public_approval": self.public_approval,
            "corruption_level": self.corruption_level,
            "active_policies": len(self.active_policies),
            "ruling_party": self.current_ruling_party.name if self.current_ruling_party else None
        }
        
    def simulate_turn(self):
        """Simulate one turn of political events"""
        # Update party support levels based on public approval
        for party in self.parties:
            if party == self.current_ruling_party:
                party.support_level += (self.public_approval - 0.5) * 0.1
            party.support_level = max(0.0, min(1.0, party.support_level))
            
        # Random events could occur here
        
        # Update overall system stability
        self.update_stability()

    def initialize_governments(self, region_count: int):
        """Initialize regional governments for all regions"""
        for region_id in range(region_count):
            self.regional_governments[region_id] = RegionalGovernment(
                region_id=region_id,
                government_type=self.government_type
            )
            
        # Initialize some basic parties
        default_parties = [
            PoliticalParty("Progressive Party", "progressive", 0.3),
            PoliticalParty("Conservative Party", "conservative", 0.3),
            PoliticalParty("Centrist Alliance", "moderate", 0.4)
        ]
        for party in default_parties:
            self.add_party(party)
            
        # Set initial ruling party
        self.current_ruling_party = self.hold_election()

    def get_regional_government(self, region_id: int) -> Optional[RegionalGovernment]:
        """Get the government for a specific region"""
        return self.regional_governments.get(region_id)

    def update_regional_government(self, region_id: int, **updates):
        """Update properties of a regional government"""
        if region_id in self.regional_governments:
            gov = self.regional_governments[region_id]
            for key, value in updates.items():
                if hasattr(gov, key):
                    setattr(gov, key, value)
                    
    def update(self, current_year: int):
        """Update the political system for the current year"""
        # Check for elections
        if current_year % self.election_cycle == 0:
            self.hold_election()
            
        # Update regional governments
        for gov in self.regional_governments.values():
            # Update local approval based on various factors
            gov.local_approval += random.uniform(-0.1, 0.1)
            gov.local_approval = max(0.0, min(1.0, gov.local_approval))
            
            # Adjust budget based on tax revenue and spending
            gov.budget += gov.tax_rate * random.uniform(100000, 1000000)  # Simplified tax collection
            gov.budget -= random.uniform(50000, 500000)  # Basic spending simulation
            
        # Update party support levels
        for party in self.parties:
            # Parties in power are more affected by public approval
            if party == self.current_ruling_party:
                party.support_level += (self.public_approval - 0.5) * 0.1
            else:
                # Opposition parties tend to gain support when public approval is low
                party.support_level += (0.5 - self.public_approval) * 0.05
            
            # Add some random fluctuation
            party.support_level += random.uniform(-0.05, 0.05)
            party.support_level = max(0.0, min(1.0, party.support_level))
            
        # Update policy effects
        for policy in self.active_policies:
            # Policies might become less effective over time
            policy.effect_strength *= 0.95
            
            # Update public approval based on policy effects
            self.public_approval += policy.effect_strength * 0.1
            
        # Random events that could affect stability
        if random.random() < 0.1:  # 10% chance of a political event
            event_impact = random.uniform(-0.2, 0.2)
            self.stability += event_impact
            self.public_approval += event_impact * 0.5
            
        # Update corruption level with small random changes
        self.corruption_level += random.uniform(-0.05, 0.05)
        self.corruption_level = max(0.0, min(1.0, self.corruption_level))
        
        # Ensure all values stay within bounds
        self.public_approval = max(0.0, min(1.0, self.public_approval))
        self.stability = max(0.0, min(1.0, self.stability))
        
        # Remove expired policies
        self.active_policies = [p for p in self.active_policies if p.effect_strength > 0.1] 