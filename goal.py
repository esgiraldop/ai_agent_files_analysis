from dataclasses import dataclass

@dataclass(frozen=True) # Inmutable classes
class Goal:
    priority: int
    name: str
    description: str

    ## Not necessary since dataclass creates this automatically
    # def __init__(self, priority, name, description):
    #     self.priority = priority
    #     self.name = name
    #     self.description = description