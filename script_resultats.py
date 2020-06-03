from CART  import *
from CHAID import *
from pickle import load
from pickle import dump

import sys
sys.setrecursionlimit(10000)

with open("arbre_cart.pickle", 'rb') as fichier:
    arbre_cart,jeu_apprentissage, jeu_test, t_cart = load(fichier)

with open("arbre_elage.pickle", 'rb') as fichier:
    arbre_elage,jeu_apprentissage, jeu_test, t_cart_elage = load(fichier)

with open("arbre_chaid.pickle", 'rb') as fichier:
    arbre_chaid,jeu_apprentissage, jeu_test, t_chaid = load(fichier)

var_cible, var_cible_pos = "final", [0,1]
print("compter_feuille(arbre_cart)", compter_feuille(arbre_cart))
print("compter_feuille(arbre_elage)", compter_feuille(arbre_elage))
#arbre_cart.afficher()
#arbre_elage.afficher()
print("\nTAUX ERREUR AVEC LE JEU DE TEST")
print("arbre :", taux_erreur_test_arbre(arbre_cart, jeu_test, var_cible, var_cible_pos))
print("arbre_elage :", taux_erreur_test_arbre(arbre_elage, jeu_test, var_cible, var_cible_pos))
print("arbre_chaid :", taux_erreur_test_arbre(arbre_chaid, jeu_test, var_cible, var_cible_pos))

print("\nTEMPS")
print("arbre_cart :", t_cart)
print("arbre_elage :", t_cart_elage)
print("arbre_chaid :", t_chaid)
