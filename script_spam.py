# import sys
# sys.setrecursionlimit(10000)

from CART import *
caracteristiques, dictionnaires = c45_interpreter("spambase.names", "spambase.data")
del(dictionnaires[0])
# dictionnaires = dictionnaires[1800:1900]
caracteristiques = caracteristiques[:-1]

jeu_apprentissage, jeu_test = choix_aleatoire_jeu_test_et_apprentissage(dictionnaires, 0.7)

arbre = creation_arbre("final", [0,1], 20, caracteristiques, jeu_apprentissage, procedure_indice_de_diversite_de_Gini)
arbre.afficher()
