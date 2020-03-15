#var_cible := la variable déterminée.
#var_cible_pos := tuple des différentes valeurs que prend var_cible (par ex: (mort, vivant) )
#min := nombre minimal d'élément dans les feuilles (à partir de 1)
#liste_caract := liste des caractéristiques sauf la var_cible
#groupe := lsite de dictionnaires (représentant les éléments)

import fonctions_d'heretogeneite

for caracteristique in liste_caract:
    #les dictionnaires de la liste sont classés par ordre croissant selon la caractéristique
    l = sorted(groupe, key=lambda variable: variable[caracteristique])
    a= [procedure_indice_de_diversite_de_Gini(groupe, var_cible_pos, caracteristique, indice_de_decoupage) for indice_de_decoupage in range(min, len(groupe)-min) ]
