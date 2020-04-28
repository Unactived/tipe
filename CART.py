from lib import *

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


def taux_erreur_noeud(noeud, jeu_test:list, var_cible, var_cible_pos):
    """associe à un noeud son taux d'erreur calculé à partir du jeu de test"""
    
    jeu_test_gauche = [dico for dico in jeu_test if dico[noeud.caracteristique] <= noeud.seuil]
    jeu_test_droite = [dico for dico in jeu_test if dico[noeud.caracteristique] > noeud.seuil]

    val_estampillee_gauche = estampillage(var_cible, var_cible_pos, jeu_test_gauche)
    val_estampillee_droite = estampillage(var_cible, var_cible_pos, jeu_test_droite)

    nombre_erreur = 0
    for i in jeu_test_gauche:
        if i[var_cible] != val_estampillee_gauche:
            nombre_erreur +=1

    for i in jeu_test_droite:
        if i[var_cible] != val_estampillee_droite:
            nombre_erreur +=1

    n = len(jeu_test)

    noeud.taux_erreur = nombre_erreur / n

def taux_erreur_arbre(noeud, jeu_test, var_cible, var_cible_pos):
    """associe à chaque noeud de l'arbre récursivement son taux d'erreur calculé à partir du jeu de test"""

    taux_erreur_noeud(noeud, jeu_test:list, var_cible, var_cible_pos)
    
    if type(noeud.gauche) == Noeud:
        jeu_test_gauche = [dico for dico in jeu_test if dico[noeud.caracteristique] <= noeud.seuil]
        taux_erreur_arbre(noeud.gauche, jeu_test_gauche, var_cible, var_cible_pos)
    
    if type(noeud.droite) == Noeud:
        jeu_test_droite = [dico for dico in jeu_test if dico[noeud.caracteristique] <= noeud.seuil]
        taux_erreur_arbre(noeud.droite, jeu_test_gauche, var_cible, var_cible_pos)

# def suppression_noeud(noeud_parent, noeud):
#     """supprime un noeud si son taux d'erreur est supérieur à son noeud parent"""

#     if noeud_parent.taux_erreur < noeud.taux_erreur:
#         del()
# def elagage(noeud, jeu_test, var_cible, var_cible_pos):
#     """supprime les noeuds de l'arbre qui diminuent la précision du modèle"""
    
#     taux_erreur_arbre(noeud, jeu_test, var_cible, var_cible_pos)

