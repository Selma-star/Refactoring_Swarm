def diviser_constante(valeurs):
    # Erreur : si valeurs est vide, len() est 0 -> Crash
    resultat = 100 / len(valeurs)
    return resultat

print(diviser_constante([]))