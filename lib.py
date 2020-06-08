"""Ressources pour arbres binaires"""

from copy import deepcopy
from random import choice


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
    __slots__ = ['caracteristique', 'seuil', 'gauche', 'droite', 'val_estampillee_gauche','val_estampillee_droite','proportion_gauche','proportion_droite', 'val_weakest_link']

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
        self.val_estampillee_gauche = None
        self.val_estampillee_droite = None
        self.proportion_gauche = None
        self.proportion_droite = None
        self.val_weakest_link = None

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

def frequence(groupe:list, caracteristique:str, var_cible_pos:tuple)->list:
    """prend en argument une liste de dictionnaires, 
    une caractéristique (qualitative)
    et une liste de valeurs de la caractéristique ;
    renvoie la liste des fréquences des éléments de groupe avec les différentes valeurs de la caractéristique"""
    frequence = [0 for i in range(len(var_cible_pos))]
    

    for element in groupe:
        final = element[caracteristique]
        if final in var_cible_pos:
            final_index = var_cible_pos.index(final)
            frequence[final_index] += 1

    n = len(groupe)
    # print("len(groupe)", len(groupe))
    for i in range(len(frequence)):
        frequence[i] /= n

    return frequence


#var_cible := la variable déterminée.
#var_cible_pos := tuple des différentes valeurs que prend var_cible (par ex: (0, 1) )
#min := nombre minimal d'élément dans les feuilles (à partir de 1)
#liste_caract := liste des caractéristiques sauf la var_cible
#groupe := liste de dictionnaires (les dictionnaires représentant les individus)

def estampillage(var_cible:str, var_cible_pos:list, groupe:list):
    """renvoie la valeur de var_cible la plus présente parmi groupe"""

    l_nb_pos = []

    for pos in var_cible_pos:
        l_nb_pos.append(len([0 for dico in groupe if dico[var_cible]==pos]))

    return var_cible_pos[l_nb_pos.index(max(l_nb_pos))]

test = 0

def creation_noeud(var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list, procedure:'function'):
    global test#pour observer en temps réel combien de noeuds ont été créé

    resultats_fonction_heterogeneite = []
    liste_des_listes_indice_de_decoupage = []
    for caracteristique in liste_caract:
        print("test,caracteristique", test, caracteristique)
        groupe = sorted(groupe, key=lambda variable: variable[caracteristique])
        #les dictionnaires de la liste sont classés par ordre croissant selon la caractéristique

        assert min <= len(groupe)-min+1, "min est trop grand"

        liste_indice_de_decoupage = []
        for i in range(min, len(groupe)-min+1):
            if groupe[i][caracteristique] != groupe[i-1][caracteristique]:
                liste_indice_de_decoupage.append(i)

        liste_des_listes_indice_de_decoupage.append(liste_indice_de_decoupage)
        
        if liste_indice_de_decoupage == []:#si la liste est vide, alors toutes les valeurs pour cette caractéristique sont identiques
            resultats_fonction_heterogeneite.append([0])#ce que renverrait procedure en n'importe quel point de decoupage
            continue

        resultats_fonction_heterogeneite.append( [ procedure(groupe, var_cible, var_cible_pos, indice_de_decoupage) for indice_de_decoupage in liste_indice_de_decoupage ] )
        #la liste créée par compréhension est la liste des valeurs renvoyées par la fonction d'hétérogénéité pour toute les valeurs possibles
        #Ainsi, dans resultats_fonction_heterogeneite, il y a une liste par caractéristiques
        
    #ici commence l'algorithme de recherche du maximum
    #pour chaque liste de resultats_fonction_heterogeneite, correspondant à une caractéristiques, on cherche le maximum.
    #Ainsi, on a le meilleur point de coupure par caractéristique.
    #Ensuite, on compare le maximum des caractéristiques. On aboutit au maximum parmi toutes les caractéristiques et toutes les valeurs, c'est-à-dire le meilleur point de coupure.

    l_max_var = [max(l) for l in resultats_fonction_heterogeneite ]

    l_max_indice = [l.index(max(l)) for l in resultats_fonction_heterogeneite ]

    
    max_f_htn = max(l_max_var) #valeur maximale de la fonction d'hétérogénéité

    if max_f_htn == 0:#équivaut au fait que le groupe soit homogène
        val_estampillee = estampillage(var_cible, var_cible_pos, groupe)
        return val_estampillee, frequence(groupe, var_cible, [val_estampillee]), len(groupe)
    
    num_caract = l_max_var.index(max_f_htn)

    caracteristique = liste_caract[num_caract]

    groupe = sorted(groupe, key=lambda variable: variable[caracteristique])

    indice_max = l_max_indice[num_caract]
    liste_indice_de_decoupage = liste_des_listes_indice_de_decoupage[num_caract]
    element_seuil = liste_indice_de_decoupage[indice_max]-1 #-1, car on regarde les valeurs <= seuil
    seuil = groupe[element_seuil][caracteristique]
  
    groupe_gauche = [dico for dico in groupe if dico[caracteristique] <= seuil]
    groupe_droite = [dico for dico in groupe if dico[caracteristique] > seuil]

    noeud = Noeud( caracteristique, seuil )

    if len(groupe_gauche) < 2*min:
        val_estampillee = estampillage(var_cible, var_cible_pos, groupe_gauche)
        noeud.gauche = val_estampillee, frequence(groupe_gauche, var_cible, [val_estampillee]), len(groupe_gauche)
    
    if len(groupe_droite) < 2*min:
        val_estampillee = estampillage(var_cible, var_cible_pos, groupe_droite)
        noeud.droite = val_estampillee, frequence(groupe_droite, var_cible, [val_estampillee]), len(groupe_droite)

    return noeud

def suite_creation_arbre(noeud_parent, var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list, procedure):
    """crée la suite d'un arbre récursivement à partir d'un certain noeud."""
    global test
    test+=1
    print(test)
    
    if type(noeud_parent) == Noeud:
        
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


def exploitation(arbre, individu):
    """Renvoie le résultat d'un arbre pour un individu"""

    noeud = deepcopy(arbre) # On évite d'altérer l'arbre

    while type(noeud) is Noeud:
        noeud = noeud.suivant(individu)

    # On obtient un triplet décrivant le noeud final
    # dont le premier élément est la valeur désirée

    return noeud[0]

def choix_aleatoire_jeu_test_et_apprentissage(groupe:list, proportion:float, var_cible, var_cible_pos):
    """prend en argument un groupe et la proportion du groupe qui doit servir de jeu d'apprentissage;
    renvoie le jeu d'apprentissage et le jeu de test"""
    liste_classes = [ [element for element in groupe if element[var_cible] == classe] for classe in var_cible_pos]
    
    jeu_apprentissage = []
    
    for classe in liste_classes:
        for i in range( int(proportion*len(classe)) ):
            element = choice(classe)
            while element in jeu_apprentissage:
                element = choice(classe)
            jeu_apprentissage.append(element)

    jeu_test = [element for element in groupe if element not in jeu_apprentissage]

    return jeu_apprentissage, jeu_test


def taux_erreur_test_arbre(arbre:Noeud, jeu_test:list, var_cible:str, var_cible_pos:list):
    """revoie le taux d'erreur de l'arbre calculé à partir du jeu de test"""

    nombre_erreur = 0

    for element in jeu_test:
        if element[var_cible] != exploitation(arbre, element):
            nombre_erreur += 1

    return nombre_erreur/len(jeu_test)
