from CHAID import *
from CART  import *
from pickle import dump
from time import perf_counter

caracteristiques, dictionnaires = c45_interpreter("spambase.names", "spambase.data")
del(dictionnaires[0])
# dictionnaires = dictionnaires[1800:1900]
caracteristiques = caracteristiques[:-1]
var_cible, var_cible_pos = "final", [0,1]

jeu_apprentissage, jeu_test = choix_aleatoire_jeu_test_et_apprentissage(dictionnaires, 0.7, var_cible, var_cible_pos)

t_cart_0 = perf_counter()
arbre_cart = creation_arbre("final", [0,1], 5, caracteristiques, jeu_apprentissage, procedure_indice_de_diversite_de_Gini)
t_cart_1 = perf_counter()

t_cart = t_cart_1 - t_cart_0

with open("arbre_cart.pickle", 'wb') as fichier:
    dump([arbre_cart,jeu_apprentissage, jeu_test, t_cart], fichier)

t_cart_elage_0 = perf_counter()
arbre_elage = elagage(arbre_cart, jeu_apprentissage, jeu_test, "final",[0,1])
t_cart_elage_1 = perf_counter()

t_cart_elage = t_cart_elage_1 - t_cart_elage_0

with open("arbre_elage.pickle", 'wb') as fichier:
    dump([arbre_elage,jeu_apprentissage, jeu_test, t_cart_elage], fichier)

t_chaid_0 = perf_counter()
arbre_chaid = creation_arbre("final", [0,1], 5, caracteristiques, jeu_apprentissage, test_khi_2)
t_chaid_1 = perf_counter()

t_chaid = t_chaid_1 - t_chaid_0

with open("arbre_chaid.pickle", 'wb') as fichier:
    dump([arbre_chaid,jeu_apprentissage, jeu_test, t_chaid], fichier)
