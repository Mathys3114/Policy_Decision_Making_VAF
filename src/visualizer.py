import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any, Set
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