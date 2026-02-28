import math


def validate_numeric(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Les arguments doivent être des nombres (int ou float).")


def add(a, b):
    validate_numeric(a, b)
    return a + b


def divide(a, b):
    validate_numeric(a, b)
    if math.isclose(float(b), 0.0, abs_tol=1e-12):
        raise ValueError("Cannot divide by zero")
    return a / b


def test():
    x = 10
    y = 5

    try:
        # Test de l'addition
        resultat_add = add(x, y)
        print(f"Resultat Addition: {resultat_add}")

        # Test de la division
        resultat_div = divide(x, y)
        print(f"Resultat Division: {resultat_div}")

        # Test de la gestion d'exception (Division par zéro)
        print("Test division par zéro :")
        divide(x, 0)

    except (TypeError, ValueError) as e:
        print(f"Erreur capturée : {e}")

    try:
        # Test de la validation des types
        print("Test validation des types :")
        add(x, "5")
    except TypeError as e:
        print(f"Erreur de type capturée : {e}")


if __name__ == "__main__":
    test()