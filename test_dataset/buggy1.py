def diviser_constante(valeurs):
    try:
        # Validation de type et calcul de la longueur
        # Gère les types non itérables via l'exception TypeError
        nb_elements = len(valeurs)
        
        # Gestion du cas division par zéro si la liste est vide
        if nb_elements == 0:
            return 0
            
        return 100 / nb_elements
    except (TypeError, ZeroDivisionError):
        # Protection contre le déni de service (DoS) en évitant les crashs
        return 0

if __name__ == "__main__":
    print(diviser_constante([]))