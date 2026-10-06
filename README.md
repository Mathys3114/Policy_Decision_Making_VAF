# Policy Decision-Making via Value-Based Argumentation Frameworks (VAF)

Plateforme d'évaluation de politiques publiques basée sur les travaux de Trevor Bench-Capon. 
Ce projet modélise des débats entre plusieurs agents ayant des préférences de valeurs différentes, en calculant les *Preferred Extensions* pour résoudre les conflits.

## 📋 Prérequis
- Python 3.8+
- Les bibliothèques `networkx` et `matplotlib` pour la visualisation graphique.

## ⚙️ Installation
Ouvrez un terminal à la racine du projet et installez les dépendances :

```bash
python -m pip install -r requirements.txt
```

## 🚀 Lancement de la Démo Interactive

```bash
python main.py
```

Une interface en ligne de commande s'ouvrira, vous permettant de :
1. Visualiser les graphes subjectifs et les arguments acceptés pour chaque agent.
2. Analyser l'agrégation finale via deux graphes de synthèse visuelle : le consensus total et les points de désaccord.
3. Modifier l'ordre de préférence des valeurs d'un agent en temps réel pour voir l'impact sur le débat.

## 📂 Architecture du Projet
- `data/` : Contient les scénarios de débats au format JSON.
- `src/models.py` : Structures de données de base (Argument, Attack, Agent).
- `src/vaf_system.py` : Logique de filtrage de Bench-Capon (Génération des graphes subjectifs).
- `src/solver.py` : Algorithmes de résolution de Dung (Grounded & Preferred Extensions).
- `src/visualizer.py` : Rendu graphique des graphes 2D (vues par agent et vues de synthèse).
- `main.py` : Point d'entrée et interface interactive.