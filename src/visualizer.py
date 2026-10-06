import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Set
from .models import Agent
from .vaf_system import VAFSystem

def draw_subjective_graph(data: Dict[str, Any], vaf: VAFSystem, agent: Agent, accepted_args: Set[str], rejected_args: Set[str], ax):
    """
    Dessine le graphe subjectif de l'agent sur un axe Matplotlib (ax) spécifique.
    """
    G = nx.DiGraph()
    
    for arg_id in data["arguments"].keys():
        G.add_node(arg_id)
        
    defeats = vaf.evaluate_defeats(agent)
    defeat_edges = [(d.attacker_id, d.target_id) for d in defeats]
    
    all_attacks = [(a.attacker_id, a.target_id) for a in data["attacks"]]
    ignored_edges = [edge for edge in all_attacks if edge not in defeat_edges]

    pos = nx.spring_layout(G, k=1.5, seed=42)
    
    node_colors = []
    for node in G.nodes():
        if node in accepted_args:
            node_colors.append('lightgreen')
        elif node in rejected_args:
            node_colors.append('lightcoral')
        else:
            node_colors.append('lightgray')

    # Titre de la sous-fenêtre
    ax.set_title(f"{agent.name}\n({', '.join(agent.preferences)})", fontsize=10, pad=10)
    
    # TAILLE DES NŒUDS
    NODE_SIZE = 2000

    # 1. Dessiner les nœuds en premier (le fond)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=NODE_SIZE, 
                           edgecolors='black', alpha=0.9, ax=ax)
    
    # 2. Dessiner les attaques IGNORÉES (par dessus les nœuds)
    nx.draw_networkx_edges(G, pos, edgelist=ignored_edges, edge_color='gray', 
                           width=1, style='dashed', arrowsize=15, node_size=NODE_SIZE, 
                           ax=ax)
                           
    # 3. Dessiner les VRAIES défaites (par dessus les attaques ignorées)
    nx.draw_networkx_edges(G, pos, edgelist=defeat_edges, edge_color='black', 
                           width=2, arrowsize=20, node_size=NODE_SIZE, 
                           ax=ax)
    
    # 4. Dessiner les labels en tout dernier (pour qu'ils soient lisibles même si une flèche passe)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)
    
    # Enlever le cadre
    ax.axis('off')

def draw_analysis_graphs(data: Dict[str, Any], consensus: List[str], disagreements: List[Any]):
    """
    Crée une nouvelle fenêtre contenant deux sous-graphes : le consensus et les désaccords.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle("Analyse Globale du Débat", fontsize=16, fontweight='bold')
    
    G = nx.DiGraph()
    for arg_id in data["arguments"].keys():
        G.add_node(arg_id)
        
    all_attacks = [(a.attacker_id, a.target_id) for a in data["attacks"]]
    pos = nx.spring_layout(G, k=1.5, seed=42)
    NODE_SIZE = 2000

    # CONSENSUS
    consensus_colors = ['lightgreen' if node in consensus else 'lightgray' for node in G.nodes()]
    ax1.set_title("Consensus Total\n(Acceptés par tous)", fontsize=14, pad=10)
    
    nx.draw_networkx_nodes(G, pos, node_color=consensus_colors, node_size=NODE_SIZE, edgecolors='black', alpha=0.9, ax=ax1)
    nx.draw_networkx_edges(G, pos, edgelist=all_attacks, edge_color='gray', width=1, arrowsize=15, node_size=NODE_SIZE, ax=ax1)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax1)
    ax1.axis('off')

    # DÉSACCORDS 
    disagreement_args = [arg for arg, agents in disagreements]
    disagree_colors = ['gold' if node in disagreement_args else 'lightgray' for node in G.nodes()]
    ax2.set_title("Points de Désaccord\n(Acceptés par certains agents uniquement)", fontsize=14, pad=10)
    
    nx.draw_networkx_nodes(G, pos, node_color=disagree_colors, node_size=NODE_SIZE, edgecolors='black', alpha=0.9, ax=ax2)
    nx.draw_networkx_edges(G, pos, edgelist=all_attacks, edge_color='gray', width=1, arrowsize=15, node_size=NODE_SIZE, ax=ax2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax2)
    ax2.axis('off')
    
    plt.tight_layout()