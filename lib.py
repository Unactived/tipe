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

def frequence(groupe:list, var_cible_pos:tuple, caracteristique:str)->list:
    """renvoie la liste des fréquences des éléments de groupe avec les valeurs de la caractéristique"""
    frequence = [0 for i in range(len(var_cible_pos))]
    
    for i in groupe:
        for j, k in enumerate(var_cible_pos):
            if i[caracteristique] == k:
                frequence[j] += 1

    n = len(groupe)

    for i in range(len(frequence)):
        frequence[i] /= n

    return frequence

#var_cible := la variable déterminée.
#var_cible_pos := tuple des différentes valeurs que prend var_cible (par ex: (mort, vivant) )
#min := nombre minimal d'élément dans les feuilles (à partir de 1)
#liste_caract := liste des caractéristiques sauf la var_cible
#groupe := lsite de dictionnaires (représentant les éléments)
def creation_noeud(var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list, procedure:function):

    resultats_fonction_heterogeneite = []
    for caracteristique in liste_caract:
        groupe = sorted(groupe, key=lambda variable: variable[caracteristique])#les dictionnaires de la liste sont classés par ordre croissant selon la caractéristique
        resultats_fonction_heterogeneite.append( [ procedure(groupe, var_cible_pos, caracteristique, indice_de_decoupage) for indice_de_decoupage in range(min, len(groupe)-min) ] )
        #la liste créée par compréhension est la liste des valeurs renvoyées par la fonction d'hétérogénéité pour toute les valeurs possibles
        #Ainsi, dans resultats_fonction_heterogeneite, il y a une liste par caractéristiques
    
    #ici commence l'algorithme de recherche du maximum
    #pour chaque liste de resultats_fonction_heterogeneite, correspondant à une caractéristiques, on cherche le minimum.
    #Ainsi, on a le meilleur point de coupure par caractéristique.
    #Ensuite, on compare le minimum des caractéristiques. On aboutit au minimum parmi toutes les caractéristiques et toutes les valeurs, càd le meilleur point de coupure.
    #On travaille sur les indices, pour garder en mémoire l'indice du minimum, puisque l'on veut à la fin savoir quel point de coupure garder, puis quelle variable étudier.
    max_indice_1 = 0
    l_max_indice_2 = []
    for indice_1 in range(len(resultats_fonction_heterogeneite)):#on cherche l'indice du minimum et le minimum de chaque sous-liste de resultats_fonction_heterogeneite
        max_indice_2 = 0
        max_var_2 = resultats_fonction_heterogeneite[indice_1][0]
        for indice_2, var_2 in enumerate( resultats_fonction_heterogeneite[indice_1] ):
            if var_2 > max_var_2:
                max_indice_2 = indice_2
                max_var_2 = var_2
        l_max_2.append( [ max_indice_2, max_var_2 ] )#on obtient un liste de sous-listes
        #Dans l_max_2, chaque sous-liste correspond à une caractéristique.
        #Une sous-liste comprend l'indice et la valeur du minimum des renvoies de la fonction d'hétérogénéité pour une caractéristiques

    #on cherche à présent le minimum entre les sous-listes
    max_var = l_max_2[0][1]
    max_indice = 0
    for i in range(len(l_max_indice_2)):
        if l_max_2[i][1] > max_var:
            max_indice = i
            max_var = l_max_2[i][1]

    Noeud( liste_caract[max_indice], l_max_2[min_indice][1], None, None)
    return  liste_caract[max_indice], l_max_2[min_indice][1] # variable à étudier, valeur seuil
