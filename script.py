# import sys
# sys.setrecursionlimit(10000)

from CART import *
caracteristiques, dictionnaires = c45_interpreter("spambase.names", "spambase.data")
del(dictionnaires[0])
dictionnaires = dictionnaires[1700:1950]
caracteristiques = caracteristiques[:-1]
# x1 = [i for i in range(1, 31)]
# x2 = [i for i in list(range(1,16))+list(range(1,16))]
# x3 = [0 for i in range(30)]
# y = [1 for i in range(2)] + [0 for i in range(28)]
# caracteristiques = ["x1", "x2"]
# dictionnaires = []
# for i in range(30):
#     dictionnaires.append( {"x1":x1[i], "x2":x2[i],"x3":x3[i], "y":y[i] } )
# for i in dictionnaires:
#     print(i)
# arbre = creation_arbre("y", [0,1], 1, caracteristiques, dictionnaires, procedure_indice_de_diversite_de_Gini)
arbre = creation_arbre("final", [0,1], 20, caracteristiques, dictionnaires, procedure_indice_de_diversite_de_Gini)
arbre.afficher()
