#var_cible := la variable déterminée.
#var_cible_pos := tuple des différentes valeurs que prend var_cible (par ex: (mort, vivant) )
#min := nombre minimal d'élément dans les feuilles (à partir de 1)
#liste_caract := liste des caractéristiques sauf la var_cible
#groupe := lsite de dictionnaires (représentant les éléments)
resultats_fonction_heterogeneite = []
for caracteristique in liste_caract:
    #les dictionnaires de la liste sont classés par ordre croissant selon la caractéristique
    groupe = sorted(groupe, key=lambda variable: variable[caracteristique])
    resultats_fonction_heterogeneite.append([procedure_indice_de_diversite_de_Gini(groupe, var_cible_pos, caracteristique, indice_de_decoupage) for indice_de_decoupage in range(min, len(groupe)-min) ] )

min_indice_1 = 0
l_min_indice_2 = []
for indice_1 in range(len(resultats_fonction_heterogeneite)):
    min_indice_2 = 0
    min_var_2 = resultats_fonction_heterogeneite[indice_1][0]
    for indice_2, var_2 in enumerate(resultats_fonction_heterogeneite[indice_1]):
        if var_2 < min_var_2:
            min_indice_2 = indice_2
            min_var_2 = var_2
    l_min_indice_2.append([min_indice_2, min_var_2 ])

min_var = l_min_indice_2[0][1]
min_indice = 0
for i in range(len(l_min_indice_2)):
    if l_min_indice_2[i][1] < min_var:
        min_indice = i
        min_var = l_min_indice_2[i][1]

print("variable à étudier :", liste_caract[min_indice], "\n valeur seuil :", l_min_indice_2[min_indice][1])
