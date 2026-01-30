class Game:
    """
    Classe représentant une instance de jeu permettant de calculer un ratio.
    """

    def __init__(self, score, total):
        """
        Initialise l'objet Game avec un score et un total.
        
        :param score: Le nombre de points obtenus.
        :param total: La valeur totale de référence.
        """
        self.score = score
        self.total = total

    def get_ratio(self):
        """
        Calcule le ratio du score par rapport au total.
        
        Retourne 0.0 si le total est égal à zéro pour éviter une exception 
        ZeroDivisionError, sinon retourne le résultat de la division.
        """
        if self.total == 0:
            return 0.0
        return self.score / self.total