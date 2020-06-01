# import sys
# sys.setrecursionlimit(10000)

from CHAID import *
caracteristiques, dictionnaires = c45_interpreter("spambase.names", "spambase.data")
del(dictionnaires[0])
# dictionnaires = dictionnaires[1800:1900]
caracteristiques = caracteristiques[:-1]

jeu_apprentissage, jeu_test = choix_aleatoire_jeu_test_et_apprentissage(dictionnaires, 0.7)

arbre = creation_arbre("final", [0,1], 400, caracteristiques, jeu_apprentissage, test_khi_2)
arbre.afficher()
