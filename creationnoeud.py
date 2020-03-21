#var_cible := la variable déterminée.
#var_cible_pos := tuple des différentes valeurs que prend var_cible (par ex: (mort, vivant) )
#min := nombre minimal d'élément dans les feuilles (à partir de 1)
#liste_caract := liste des caractéristiques sauf la var_cible
#groupe := lsite de dictionnaires (représentant les éléments)
def creation_noeud(var_cible:str, var_cible_pos:list, min:int, liste_caract:list, groupe:list):

    resultats_fonction_heterogeneite = []
    for caracteristique in liste_caract:
        groupe = sorted(groupe, key=lambda variable: variable[caracteristique])#les dictionnaires de la liste sont classés par ordre croissant selon la caractéristique
        resultats_fonction_heterogeneite.append( [ procedure_indice_de_diversite_de_Gini(groupe, var_cible_pos, caracteristique, indice_de_decoupage) for indice_de_decoupage in range(min, len(groupe)-min) ] )
        #la liste créée par compréhension est la liste des valeurs renvoyées par la fonction d'hétérogénéité pour toute les valeurs possibles
        #Ainsi, dans resultats_fonction_heterogeneite, il y a une liste par caractéristiques
    
    #ici commence l'algorithme de recherche du minimum (IL FAUT TOUT CHANGER -> MAX)
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

    return  liste_caract[max_indice], l_max_2[min_indice][1] # variable à étudier, valeur seuil
