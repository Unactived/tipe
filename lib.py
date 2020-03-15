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
    __slots__ = ['caracteristique', 'seuil', 'gauche', 'droite']

    def __init__(self, caracteristique: str, seuil: float, gauche, droite):
        """
        Constructeur de la classe, prend 4 arguments.
        Ne fait que les assigner aux attributs de même nom.

        """

        self.caracteristique = caracteristique
        self.seuil = seuil
        self.gauche = gauche
        self.droite = droite

    def suivant(self, dico: dict):
        """
        Compare la valeur du dictionnaire en argument, indexée par la caractéristique du noeud,
        à la valeur seuil du noeud et renvoie l'attribut gauche ou droite selon le résultat de leur comparaison.

        """

        if dico[self.caracteristique] <= self.seuil:
            return self.gauche

        return self.droite

def _c45_parser(fichier_names: str) -> list:
    """
    Parse le fichier .names d'un dataset au format C4.5

    Renvoie les caractéristiques d'une instance considérée.
    """

    with open(fichier_names, 'r') as fichier:
        lignes = fichier.read().split('\n')

    classes_definies = False
    caracteristiques = []

    # On retire les commentaires, signalés par '|'
    # Le point suivi d'un espace termine la ligne
    for ligne in lignes:
        index = ligne.find('|')

        if index != -1:
            ligne = ligne[:index]

        index = ligne.find('. ') # l'espace après le point est significatif

        if index != -1:
            ligne = ligne[:index]

        if not ligne: # ligne vide
            continue

        if ligne.endswith('.'):
            ligne = ligne[:-1] # le point final est faculatif, tout comme l'espace le suivant

        if not classes_definies:
            # La première vraie ligne est l'énumération des classes finales possibles
            classes = [word.strip() for word in ligne.split(',')] # Inutilisé, il s'agit des valeurs finales possibles
            classes_definies = True
        else:
            caracteristiques.append(ligne[:ligne.index(':')].strip())

    caracteristiques.append("final") # Le dernier champ est le résultat

    return caracteristiques

def c45_interpreter(fichier_names: str, fichier_data: str):
    """
    Prend en argument le chemin du fichier contenant la description du set
    et le chemin du fichier contenant les données du set

    Renvoie la liste des caractéristiques ainsi qu'une liste de dictionnaires,
    chaque dictionnaire étant une instance indexée par ses caractéristiques

    """

    caracteristiques = _c45_parser(fichier_names)

    with open(fichier_data, 'r') as fichier:
        lignes = fichier.read().split('\n')

    dictionnaires = []

    for ligne in lignes:
        dico = {}
        valeurs = ligne.split(',')

        for caracteristique, valeur in zip(caracteristiques, valeurs):
            # À moins d'utiliser des regex, seule façon réellement correcte
            try:
                valeur = int(valeur)
            except ValueError:
                try:
                    valeur = float(valeur)
                except ValueError:
                    pass
            dico[caracteristique] = valeur

        dictionnaires.append(dico)

    return caracteristiques, dictionnaires
