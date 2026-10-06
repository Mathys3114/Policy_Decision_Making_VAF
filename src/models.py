from dataclasses import dataclass
from typing import List

@dataclass
class Argument:
    """Représente un argument dans le débat"""
    id: str
    text: str
    value: str

    def __repr__(self) -> str:
        return f"[{self.id}] {self.text[:30]}... (Valeur: {self.value})"

@dataclass
class Attack:
    """Représente une attaque logique (Dung) entre deux arguments"""
    attacker_id: str
    target_id: str

    def __repr__(self) -> str:
        return f"{self.attacker_id} -> {self.target_id}"

class Agent:
    """Représente une audience avec ses préférences de valeurs"""
    def __init__(self, name: str, preferences: List[str]):
        self.name = name
        self.preferences = preferences  # Ordre décroissant : [Le plus important > ... > Le moins important]

    def prefers(self, val1: str, val2: str) -> bool:
        """
        Retourne True si val1 est strictement préférée à val2
        Dans une liste, l'index le plus bas est le plus préféré (index 0 > index 1)
        """
        if val1 not in self.preferences or val2 not in self.preferences:
            return False
        return self.preferences.index(val1) < self.preferences.index(val2)

    def __repr__(self) -> str:
        return f"Agent({self.name} | Préférences: {' > '.join(self.preferences)})"