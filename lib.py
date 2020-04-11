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

    def __init__(self, caracteristique: str, seuil: float):
        """
        Constructeur de la classe, prend 2 arguments.
        Ne fait que les assigner aux attributs de même nom, et créer deux emplacements
        pour les noeuds suivants.

        """

        self.caracteristique = caracteristique
        self.seuil = seuil
        self.gauche = None
        self.droite = None

    def suivant(self, dico: dict):
        """
        Compare la valeur du dictionnaire en argument, indexée par la caractéristique du noeud,
        à la valeur seuil du noeud et renvoie l'attribut gauche ou droite selon le résultat de leur comparaison.

        """

        if dico[self.caracteristique] <= self.seuil:
            return self.gauche

        return self.droite

    def afficher(self, *args):
        """
        Affiche la structure du noeud et des noeuds en dépendant
        Les paramètres mis en jeu servent à la construction du résultat
        et ne devraient pas être explicitement déclarés par l'utilisateur
        (ne faire que noeud.afficher()).

        La fonction renvoie None à l'utilisateur (durant la récursion
        la fonction se renvoie une liste de chaînes de caractères).

        Inspiré de solutions analogues en Java et Scala.

        """

        if not args:
            # On initialise la récursion et affiche le futur résultat
            constructeur = []
            return print("\n".join(self.afficher([], "", "")))

        constructeur, prefixe, prefixe_suivant = args

        constructeur.append(f"{prefixe}{self.caracteristique}, {str(self.seuil)}")

        gauche = self.gauche
        droite = self.droite

        if not type(gauche) is Noeud:
            constructeur.append(f"{prefixe_suivant}├── {str(gauche)}")
        else:
            gauche.afficher(constructeur, prefixe_suivant + "├── ", prefixe_suivant + "│   ")

        if not type(droite) is Noeud:
            constructeur.append(f"{prefixe_suivant}└── {str(droite)}")
        else:
            droite.afficher(constructeur, prefixe_suivant + "└── ", prefixe_suivant + "    ")

        return constructeur

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

        manque = False

        for caracteristique, valeur in zip(caracteristiques, valeurs):
            # À moins d'utiliser des regex, seule façon réellement correcte
            try:
                valeur = int(valeur)
            except ValueError:
                try:
                    valeur = float(valeur)
                except ValueError:
                    if not valeur:
                        manque = True
                        break
            dico[caracteristique] = valeur

        if not manque:
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
#groupe := liste de dictionnaires (représentant les éléments)

def estampillage(var_cible:str, var_cible_pos:list, groupe:list):
    """renvoie la valeur de var_cible la plus présente parmi groupe"""
    
    l_nb_pos = []
    
    for pos in var_cible_pos:    
        l_nb_pos.append(len([0 for dico in groupe if dico[var_cible]==pos]))
    
    return var_cible_pos[l_nb_pos.index(max(l_nb_pos))]

test = 0

def creation_noeud(var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list, procedure:'function'):
    global test
    # print("len(groupe)",len(groupe))
    # if len(groupe) <= 2*min:
    #     print("Groupe donné en entrée trop petit")
    #     return False
    
    resultats_fonction_heterogeneite = []
    for caracteristique in liste_caract:
        print(test,caracteristique)
        groupe = sorted(groupe, key=lambda variable: variable[caracteristique])#les dictionnaires de la liste sont classés par ordre croissant selon la caractéristique
        # print("list(range(min, len(groupe)-min+1))", list(range(min, len(groupe)-min+1)))
        resultats_fonction_heterogeneite.append( [ procedure(groupe, var_cible_pos, caracteristique, indice_de_decoupage) for indice_de_decoupage in range(min, len(groupe)-min+1) ] )
        #la liste créée par compréhension est la liste des valeurs renvoyées par la fonction d'hétérogénéité pour toute les valeurs possibles
        #Ainsi, dans resultats_fonction_heterogeneite, il y a une liste par caractéristiques
    
    #ici commence l'algorithme de recherche du maximum
    #pour chaque liste de resultats_fonction_heterogeneite, correspondant à une caractéristiques, on cherche le maximum.
    #Ainsi, on a le meilleur point de coupure par caractéristique.
    #Ensuite, on compare le maximum des caractéristiques. On aboutit au maximum parmi toutes les caractéristiques et toutes les valeurs, càd le meilleur point de coupure.
    #On travaille sur les indices, pour garder en mémoire l'indice du maximum, puisque l'on veut à la fin savoir quel point de coupure garder, puis quelle variable étudier.
    #on cherche l'indice du maximum et le maximum de chaque sous-liste de resultats_fonction_heterogeneite
    l_max_var = [max(l) for l in resultats_fonction_heterogeneite]
    l_max_indice = [l.index(max(l)) for l in resultats_fonction_heterogeneite]
    # print(l_max_var)
    max_f_htn = max(l_max_var) #valeur maximale de la fonction d'hétérogénéité
    num_caract = l_max_var.index(max_f_htn)
    caracteristique = liste_caract[num_caract]
    
    groupe = sorted(groupe, key=lambda variable: variable[caracteristique])
    seuil = groupe[l_max_indice[num_caract] + min - 1][caracteristique]

    # print("seuil", seuil)
    # for i in groupe:
    #     print("i[caracteristique]", i[caracteristique], "caracteristique",caracteristique)
        
    groupe_gauche = [dico for dico in groupe if dico[caracteristique] <= seuil]
    groupe_droite = [dico for dico in groupe if dico[caracteristique] > seuil]
    # print("groupe == groupe_gauche",groupe == groupe_gauche)
    val_gauche = None
    val_droite = None
    # print("len(groupe_gauche)", len(groupe_gauche), "len(groupe_droite)", len(groupe_droite))
    if len(groupe_gauche) <= 2*min-1:
        val_gauche = estampillage(var_cible, var_cible_pos, groupe_gauche)
    
    if len(groupe_droite) <= 2*min-1:
        val_droite = estampillage(var_cible, var_cible_pos, groupe_droite)
    
    noeud = Noeud( liste_caract[num_caract], seuil )
    # print("val_gauche", val_gauche, "val_droite", val_droite)
    noeud.gauche = val_gauche
    noeud.droite = val_droite
    
    noeud.afficher()
    
    return noeud

def suite_creation_arbre(noeud_parent, var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list, procedure):
    """crée la suite d'un arbre récursivement à partir d'un certain noeud."""
    global test
    test+=1
    print(test)
    
    if type(noeud_parent) == Noeud:#si noeud_parent n'est pas une feuille
        
        if noeud_parent.gauche == None:
            
            groupe = sorted(groupe, key=lambda variable: variable[noeud_parent.caracteristique])
            groupe_gauche = [dico for dico in groupe if dico[noeud_parent.caracteristique] <= noeud_parent.seuil]
            noeud_parent.gauche = creation_noeud(var_cible, var_cible_pos, min, liste_caract, groupe_gauche, procedure)
            suite_creation_arbre(noeud_parent.gauche, var_cible, var_cible_pos, min, liste_caract, groupe_gauche, procedure)

        if noeud_parent.droite == None:
            
            groupe = sorted(groupe, key=lambda variable: variable[noeud_parent.caracteristique])
            groupe_droite = [dico for dico in groupe if dico[noeud_parent.caracteristique] > noeud_parent.seuil]
            noeud_parent.droite = creation_noeud(var_cible, var_cible_pos, min, liste_caract, groupe_droite, procedure)
            suite_creation_arbre(noeud_parent.droite, var_cible, var_cible_pos, min, liste_caract, groupe_droite, procedure)

def creation_arbre(var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list, procedure):
    """crée un arbre"""

    noeud_parent = creation_noeud(var_cible, var_cible_pos, min, liste_caract, groupe, procedure)
    suite_creation_arbre(noeud_parent,var_cible, var_cible_pos, min, liste_caract, groupe, procedure)
    
    return noeud_parent
