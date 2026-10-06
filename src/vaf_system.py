from typing import Dict, List
from .models import Argument, Attack, Agent

class VAFSystem:
    """
    Value-Based Argumentation Framework
    Il stocke le graphe global et génère les graphes subjectifs par agent
    """
    def __init__(self, arguments: Dict[str, Argument], attacks: List[Attack]):
        self.arguments = arguments
        self.attacks = attacks

    def evaluate_defeats(self, agent: Agent) -> List[Attack]:
        """
        Filtre les attaques globales pour ne garder que celles qui réussissent (les défaites)
        selon l'ordre de préférence des valeurs de l'agent
        """
        defeats = []
        
        for attack in self.attacks:
            attacker_arg = self.arguments[attack.attacker_id]
            target_arg = self.arguments[attack.target_id]

            # RÈGLE DE BENCH-CAPON :
            # Une attaque (A -> B) devient une défaite SAUF SI l'agent préfère strictement la valeur de B à la valeur de A.
            if not agent.prefers(target_arg.value, attacker_arg.value):
                defeats.append(attack)
                
        return defeats

    def get_subjective_graph(self, agent: Agent) -> Dict[str, List[str]]:
        """
        Génère le graphe orienté (Framework de Dung) spécifique à cet agent
        Retourne un dictionnaire { target_id: [liste des attacker_ids valides] }
        """
        # Chaque argument a une liste d'attaquants vide au départ
        graph = {arg_id: [] for arg_id in self.arguments.keys()}
        
        # Récupération des défaites subjectives
        defeats = self.evaluate_defeats(agent)
        
        # Remplissage du graphe
        for defeat in defeats:
            graph[defeat.target_id].append(defeat.attacker_id)
            
        return graph