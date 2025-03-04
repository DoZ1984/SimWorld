import random

class NameGenerator:
    FIRST_NAMES = ["Juan", "María", "Carlos", "Ana", "Luis", "Laura"]
    LAST_NAMES = ["García", "Rodríguez", "González", "Fernández", "López"]
    
    @classmethod
    def generate_name(cls):
        return f"{random.choice(cls.FIRST_NAMES)} {random.choice(cls.LAST_NAMES)}" 