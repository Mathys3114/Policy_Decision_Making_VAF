import json
from typing import Dict, Any
from .models import Argument, Attack, Agent

def load_vaf_data(filepath: str) -> Dict[str, Any]:
    """
    Parse le fichier JSON et retourne un dictionnaire avec les objets Python (Arguments, Attaques, Agents).
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {filepath} est introuvable.")
        return {}
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {filepath} n'est pas un JSON valide.")
        return {}

    # Parsing des Arguments (Dict)
    arguments_dict = {}
    for arg_data in data.get("arguments", []):
        arg = Argument(
            id=arg_data["id"],
            text=arg_data["text"],
            value=arg_data["value"]
        )
        arguments_dict[arg.id] = arg

    # Parsing des Attaques (liste)
    attacks_list = []
    for att_data in data.get("attacks", []):
        attack = Attack(
            attacker_id=att_data["attacker"],
            target_id=att_data["target"]
        )
        attacks_list.append(attack)

    # Parsing des Agents (liste)
    agents_list = []
    for agent_data in data.get("agents", []):
        agent = Agent(
            name=agent_data["name"],
            preferences=agent_data["preferences"]
        )
        agents_list.append(agent)

    # dictionnaire qui servira au VAF_System
    return {
        "scenario_name": data.get("scenario_name", "Scénario Inconnu"),
        "values": data.get("values", []),
        "arguments": arguments_dict,
        "attacks": attacks_list,
        "agents": agents_list
    }