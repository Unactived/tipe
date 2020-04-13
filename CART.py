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
