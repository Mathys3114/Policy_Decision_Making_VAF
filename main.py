import os
import matplotlib.pyplot as plt
from src.parser import load_vaf_data
from src.vaf_system import VAFSystem
from src.solver import compute_preferred_extensions
from src.visualizer import draw_subjective_graph, draw_analysis_graphs

# Codes couleurs ANSI pour styliser la démo dans le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def clear_terminal():
    """Nettoie l'écran du terminal pour une interface propre."""
    os.system('cls' if os.name == 'nt' else 'clear')

def analyze_debate_consensus(data, agent_results):
    print(f"\n{Colors.BLUE}=== ANALYSE DES ACCORDS ET DÉSACCORDS ==={Colors.RESET}")
    
    arg_acceptance = {}
    for agent_name, accepted_args in agent_results.items():
        for arg in accepted_args:
            if arg not in arg_acceptance:
                arg_acceptance[arg] = []
            arg_acceptance[arg].append(agent_name)
            
    consensus = []
    disagreements = []
    num_agents = len(agent_results)
    
    for arg, agents in arg_acceptance.items():
        if len(agents) == num_agents:
            consensus.append(arg)
        else:
            disagreements.append((arg, agents))
            
    # Affichage du Consensus
    print(f"{Colors.GREEN}\n🤝 CONSENSUS TOTAL (Accepté par tous) :{Colors.RESET}")
    if not consensus:
        print("  Aucun argument ne fait l'unanimité.")
    else:
        for arg in consensus:
            print(f"  ✅ [{arg}] : {data['arguments'][arg].text}")
            
    # Affichage des Désaccords
    print(f"{Colors.YELLOW}\n⚡ POINTS DE DÉSACCORD :{Colors.RESET}")
    if not disagreements:
        print("  Tout le monde est d'accord sur les arguments retenus.")
    else:
        for arg, agents in disagreements:
            print(f"  ⚠️ [{arg}] est soutenu UNIQUEMENT par : {', '.join(agents)}")
            print(f"     -> {data['arguments'][arg].text}")
    print("\n" + "="*50)
    
    draw_analysis_graphs(data, consensus, disagreements)

def display_debate_results(data, vaf):
    clear_terminal()
    print(f"{Colors.BLUE}=== RÉSULTATS DU DÉBAT ==={Colors.RESET}\n")
    
    n_agents = len(data["agents"])
    fig, axes = plt.subplots(1, n_agents, figsize=(6 * n_agents, 7))
    fig.suptitle(f"Comparaison des Graphes - {data['scenario_name']}", fontsize=16, fontweight='bold')
    
    if n_agents == 1:
        axes = [axes]
    
    agent_results = {}
    
    for i, agent in enumerate(data["agents"]):
        print(f"Agent : {Colors.YELLOW}{agent.name}{Colors.RESET}")
        print(f"Préférences : {' > '.join(agent.preferences)}")
        
        subjective_graph = vaf.get_subjective_graph(agent)
        extensions = compute_preferred_extensions(subjective_graph)
        
        if extensions:
            first_ext = extensions[0]
            rejected = set(data["arguments"].keys()) - first_ext
        else:
            first_ext = set()
            rejected = set(data["arguments"].keys())
            
        agent_results[agent.name] = first_ext
        
        print(f"  {Colors.GREEN}✅ Preferred Extension(s) : {len(extensions)}{Colors.RESET}")
        for j, ext in enumerate(extensions):
            print(f"  -- Option {j + 1} --")
            for arg_id in ext:
                print(f"     ✅ [{arg_id}] : {data['arguments'][arg_id].text}")
        print("-" * 50)
        
        draw_subjective_graph(data, vaf, agent, first_ext, rejected, ax=axes[i])
    
    analyze_debate_consensus(data, agent_results)
    
    print("  Affichage des graphes... (Fermez la fenêtre Matplotlib pour continuer)")
    plt.tight_layout()
    plt.show()

def modify_agent_preferences(data):
    """Interface interactive pour modifier l'ordre des valeurs d'un agent."""
    print(f"\n{Colors.BLUE}=== MODIFIER LES PRÉFÉRENCES ==={Colors.RESET}")
    
    # Choix de l'agent
    for i, agent in enumerate(data["agents"]):
        print(f"{i + 1}. {agent.name} (Actuel: {' > '.join(agent.preferences)})")
    
    try:
        agent_idx = int(input("\nChoisissez le numéro de l'agent à modifier (0 pour annuler) : ")) - 1
        if agent_idx == -1: return
        
        target_agent = data["agents"][agent_idx]
    except (ValueError, IndexError):
        print(f"{Colors.RED}Choix invalide.{Colors.RESET}")
        return

    # Saisie des nouvelles préférences
    available_values = data["values"]
    print(f"\nValeurs disponibles : {', '.join(available_values)}")
    print("Entrez le nouvel ordre séparé par des virgules (ex: Economy, Social, Environment)")
    
    new_order_str = input("Nouvel ordre : ")
    
    # Nettoyage et validation de l'entrée utilisateur
    new_order = [v.strip() for v in new_order_str.split(',')]
    
    # On vérifie que l'utilisateur a bien entré toutes les valeurs exactes
    if set(new_order) == set(available_values) and len(new_order) == len(available_values):
        target_agent.preferences = new_order
        print(f"{Colors.GREEN}Préférences mises à jour avec succès !{Colors.RESET}")
    else:
        print(f"{Colors.RED}Erreur : Les valeurs saisies ne correspondent pas à la liste exacte.{Colors.RESET}")
        print("Vérifiez l'orthographe et n'oubliez aucune valeur.")

def main():
    # Chargement initial
    data = load_vaf_data("data/debate_scenario.json")
    if not data:
        return
    
    vaf = VAFSystem(data["arguments"], data["attacks"])
    
    # Boucle de l'application interactive
    while True:
        print(f"\n{Colors.BLUE}=== DÉMO VAF : {data['scenario_name']} ==={Colors.RESET}")
        print("1. Voir les résultats actuels du débat")
        print("2. Modifier les préférences d'un agent")
        print("3. Quitter")
        
        choice = input("\nVotre choix : ")
        
        if choice == '1':
            display_debate_results(data, vaf)
        elif choice == '2':
            modify_agent_preferences(data)
        elif choice == '3':
            print("Fin de la démo.")
            break
        else:
            print(f"{Colors.RED}Choix invalide.{Colors.RESET}")

if __name__ == "__main__":
    clear_terminal()
    main()