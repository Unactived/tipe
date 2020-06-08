from lib import *
from copy import deepcopy


# fonction d'hétérogénéité ___________________________________________________________________________


def fonction_indice_de_Gini(frequence:list)->float:
    """fonction d'hétérogénéité calculant l'indice de diversité de Gini"""
    
    somme = 0
    
    for i in frequence:
        somme += i**2

    return 1 - somme


def procedure_indice_de_diversite_de_Gini(groupe:list, var_cible:str, var_cible_pos:tuple, indice_de_decoupage:int)->float:
    """prend en argument un groupe d'éléments (liste de dictionnaires), les valeurs que peut prendre la variable cible (tuple), une caractéristique (chaîne de caractère) et indice_de_decoupage; 
    divise la liste en deux groupes selon le nombre d'élément à mettre dans l'un des groupes (indice_de_decoupage) ; 
    renvoie indice de Gini(avant séparation) - [ indice de Gini(gauche) + indice de Gini(droite) ] """
    
    taille_groupe_parent = len(groupe)
    proportion_gauche = len(groupe[:indice_de_decoupage]) / taille_groupe_parent
    proportion_droite = len(groupe[indice_de_decoupage:]) / taille_groupe_parent

    frequence_parent = frequence(groupe, var_cible, var_cible_pos)
    frequence_gauche = frequence(groupe[:indice_de_decoupage], var_cible, var_cible_pos)
    frequence_droite = frequence(groupe[indice_de_decoupage:], var_cible, var_cible_pos)

    Gini_parent = fonction_indice_de_Gini(frequence_parent) #indice de Gini avant séparation
    Gini_gauche = fonction_indice_de_Gini(frequence_gauche)
    Gini_droite = fonction_indice_de_Gini(frequence_droite)

    return  Gini_parent - (proportion_gauche*Gini_gauche + proportion_droite*Gini_droite)


# élagage ___________________________________________________________________________


def estampillage_arbre(noeud:Noeud, jeu_apprentissage:list, var_cible, var_cible_pos):
    """associe à chaque noeud d'un arbre la valeur de var_cible la plus présente."""

    if type(noeud) == Noeud:
        
        n = len(jeu_apprentissage)
        
        jeu_apprentissage_gauche = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] <= noeud.seuil]
        noeud.proportion_gauche = len(jeu_apprentissage_gauche) / n
        noeud.val_estampillee_gauche = estampillage(var_cible, var_cible_pos, jeu_apprentissage_gauche)
        
        jeu_apprentissage_droite = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] > noeud.seuil]
        noeud.proportion_droite = len(jeu_apprentissage_droite) / n
        noeud.val_estampillee_droite = estampillage(var_cible, var_cible_pos, jeu_apprentissage_droite)

    if type(noeud.gauche) == Noeud:
        estampillage_arbre(noeud.gauche, jeu_apprentissage_gauche, var_cible, var_cible_pos)

    if type(noeud.droite) == Noeud:
        estampillage_arbre(noeud.droite, jeu_apprentissage_droite, var_cible, var_cible_pos)


def compter_feuille(noeud:Noeud):
    """prend en argument un noeud ;
    renvoie le nombre de feuilles de l'arbre issu de noeud"""

    if type(noeud) != Noeud:
        return 1

    return compter_feuille(noeud.gauche) + compter_feuille(noeud.droite)


def taux_erreur_apprentissage_noeud(noeud:Noeud, jeu_apprentissage:list, var_cible, var_cible_pos)->float:
    """associe à un noeud son taux d'erreur calculé à partir du jeu d'apprentissage"""
    
    jeu_apprentissage_gauche = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] <= noeud.seuil]
    jeu_apprentissage_droite = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] > noeud.seuil]

    val_estampillee_gauche = noeud.val_estampillee_gauche
    val_estampillee_droite = noeud.val_estampillee_droite

    nombre_erreur = 0
    
    for i in jeu_apprentissage_gauche:
        if i[var_cible] != val_estampillee_gauche:
            nombre_erreur +=1

    for i in jeu_apprentissage_droite:
        if i[var_cible] != val_estampillee_droite:
            nombre_erreur +=1

    n = len(jeu_apprentissage)

    return nombre_erreur / n


def taux_erreur_apprentissage_arbre(noeud:Noeud, jeu_apprentissage:list, var_cible, var_cible_pos)->float:
    """associe à un arbre son taux d'erreur calculé à partir du jeu d'apprentissage"""

    jeu_apprentissage_gauche = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] <= noeud.seuil]
    jeu_apprentissage_droite = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] > noeud.seuil]
    
    if type(noeud.gauche) == Noeud:
        taux_gauche = taux_erreur_apprentissage_arbre(noeud.gauche, jeu_apprentissage_gauche, var_cible, var_cible_pos)
    
    
    else:#si c'est une feuille
        val_estampillee_gauche = noeud.val_estampillee_gauche
        nombre_erreur = 0
        
        for i in jeu_apprentissage_gauche:
            if i[var_cible] != val_estampillee_gauche:
                nombre_erreur +=1
        
        taux_gauche = nombre_erreur / len(jeu_apprentissage_gauche)

    if type(noeud.droite) == Noeud:
        taux_droite = taux_erreur_apprentissage_arbre(noeud.droite, jeu_apprentissage_droite, var_cible, var_cible_pos)
    
    else:
        val_estampillee_droite = noeud.val_estampillee_droite
        nombre_erreur = 0
        
        for i in jeu_apprentissage_droite:
            if i[var_cible] != val_estampillee_droite:
                nombre_erreur +=1
        
        taux_droite = nombre_erreur / len(jeu_apprentissage_droite)
    
    return noeud.proportion_gauche*taux_gauche + noeud.proportion_droite*taux_droite


def fonction_weakest_link(noeud:Noeud, jeu_apprentissage:list, var_cible:str, var_cible_pos:list):
    """associe à chaque noeud d'un arbre le résultat de la fonction de la méthode "weakest link pruning" """

    if type(noeud) == Noeud:
        
        taux_noeud = taux_erreur_apprentissage_noeud(noeud, jeu_apprentissage, var_cible, var_cible_pos)
        taux_arbre = taux_erreur_apprentissage_arbre(noeud, jeu_apprentissage, var_cible, var_cible_pos)
        feuilles = compter_feuille(noeud)
        
        noeud.val_weakest_link = ( taux_noeud - taux_arbre ) / ( feuilles - 1)
        
        jeu_apprentissage_gauche = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] <= noeud.seuil]
        jeu_apprentissage_droite = [dico for dico in jeu_apprentissage if dico[noeud.caracteristique] > noeud.seuil]
        fonction_weakest_link(noeud.gauche, jeu_apprentissage_gauche, var_cible, var_cible_pos)
        fonction_weakest_link(noeud.droite, jeu_apprentissage_droite, var_cible, var_cible_pos)


def ensemble_noeud_recursif(noeud:Noeud, liste_noeud:list):
    """modifie liste_noeud qui contiendra l'ensemble des noeuds de l'arbre donné en entrée"""
    
    if type(noeud) == Noeud:
        liste_noeud.append(noeud)

        ensemble_noeud_recursif(noeud.gauche, liste_noeud)
        ensemble_noeud_recursif(noeud.droite, liste_noeud)


def ensemble_noeud(noeud:Noeud)->list:
    """revoie la liste contenant l'ensemble des noeuds de l'arbre donné en entrée"""
    
    liste_noeud = []
    ensemble_noeud_recursif(noeud, liste_noeud)

    return liste_noeud


def sous_arbre_optimal(liste_noeud:list):
    """renvoie le sous-arbre optimal de noeud"""
    
    liste_noeud_parent = [noeud for noeud in liste_noeud if type(noeud.gauche) == Noeud or type(noeud.droite) == Noeud]

    noeud_weakest_link = [noeud for noeud in liste_noeud_parent if noeud.val_weakest_link == min([ noeud.val_weakest_link for noeud in liste_noeud_parent]) ]

    for noeud in noeud_weakest_link:

        noeud.gauche = [ noeud.val_estampillee_gauche ]

        noeud.droite = [ noeud.val_estampillee_droite ]


def elagage(arbre:Noeud, jeu_apprentissage:list, jeu_test:list, var_cible:str, var_cible_pos:list)->Noeud:
    """renvoie l'arbre élagué """

    estampillage_arbre(arbre, jeu_apprentissage, var_cible, var_cible_pos)

    fonction_weakest_link(arbre, jeu_apprentissage, var_cible, var_cible_pos)

    sous_arbre = deepcopy(arbre)
    liste_noeud = ensemble_noeud(sous_arbre)
    sous_arbre_optimal(liste_noeud)
    liste_sous_arbre = [arbre, sous_arbre]

    while type(sous_arbre.gauche) == Noeud or type(sous_arbre.droite) == Noeud:
        
        arbre = liste_sous_arbre[-1]
        fonction_weakest_link(arbre, jeu_apprentissage, var_cible, var_cible_pos)
        
        sous_arbre = deepcopy(arbre)
        liste_noeud = ensemble_noeud(sous_arbre)

        sous_arbre_optimal(liste_noeud)

        liste_sous_arbre.append( sous_arbre )

    liste_erreur_test = [ taux_erreur_test_arbre(arbre, jeu_test, var_cible, var_cible_pos) for arbre in liste_sous_arbre]

    indice_min = liste_erreur_test.index(min(liste_erreur_test))
    
    return liste_sous_arbre[indice_min]
