"""Ressources pour arbres binaires"""

# Commentaires temporaires
# ceci pourrait être utilisé à la fois par CART et CHAID
#
# pour rappel, depuis un noeud on "passe à" (renvoie)
# gauche si la valeur X est inférieure ou égale à seuil ;
# droite sinon i.e. la valeur X est strictement supérieure à seuil

class Noeud:
    """
    Classe représentant un noeud de l'arbre

    Typiquement un noeud contient 2 éléments, qui sont:
    - d'autres objets de la classe Noeud ou une valeur d'arrivée, un booléen dans notre cas,
    - la valeur seuil qui détermine quel objet renvoyer entre gauche et droite.

    """

    # ceci fixe les attributs possibles de la classe
    # cela permet notamment de grandement réduire la mémoire utilisée
    __slots__ = ['seuil', 'gauche', 'droite']

    def __init__(self, seuil: float, gauche, droite):
        """
        Constructeur de la classe, prend 3 arguments.
        Ne fait que les assigner aux attributs de même nom.

        """

        self.seuil = seuil
        self.gauche = gauche
        self.droite = droite

    def suivant(self, valeur: float):
        """
        Compare la valeur passée en argument à la valeur seuil du noeud
        et renvoie l'attribut gauche ou droite selon le résultat de leur comparaison.

        """

        if valeur <= self.seuil:
            return self.gauche
        else:
            return self.droite
