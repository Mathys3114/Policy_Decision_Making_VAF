from itertools import chain, combinations
from typing import Dict, List, Set

def get_powerset_descending(iterable):
    """
    Génère toutes les combinaisons possibles d'une liste, en commençant par la plus grande
    Ex: [1,2,3] -> (1,2,3), (1,2), (1,3), (2,3), (1,), (2,), (3,), ()
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s), -1, -1))

def compute_preferred_extensions(graph: Dict[str, List[str]]) -> List[Set[str]]:
    """
    Calcule toutes les Preferred Extensions du graphe subjectif
    Retourne une liste contenant un ou plusieurs ensembles (sets) d'arguments.
    """
    arguments = list(graph.keys())
    preferred_extensions = []

    def is_conflict_free(subset: Set[str]) -> bool:
        for arg in subset:
            # L'ensemble est invalide si un attaquant de 'arg' est aussi dans l'ensemble
            if any(attacker in subset for attacker in graph[arg]):
                return False
        return True

    def is_admissible(subset: Set[str]) -> bool:
        if not is_conflict_free(subset):
            return False
            
        for arg in subset:
            for attacker in graph[arg]:
                # L'argument est attaqué. Y a-t-il un défenseur dans notre sous-ensemble ?
                # càd: est-ce qu'un membre de 'subset' attaque 'attacker' ?
                is_defended = any(defender in subset for defender in graph[attacker])
                if not is_defended:
                    return False
        return True

    # On teste toutes les combinaisons, de la plus grande à la plus petite
    for subset_tuple in get_powerset_descending(arguments):
        subset = set(subset_tuple)
        
        if is_admissible(subset):
            # Comme on commence par les plus grands ensembles, le premier ensemble
            # admissible qu'on trouve est forcément Maximal (Preferred).
            # On doit juste vérifier qu'il n'est pas un sous-ensemble d'une extension préférée déjà trouvée.
            is_maximal = True
            for pref in preferred_extensions:
                if subset.issubset(pref):
                    is_maximal = False
                    break
                    
            if is_maximal:
                preferred_extensions.append(subset)

    return preferred_extensions