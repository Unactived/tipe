from lib import *
def test_khi_2(groupe:list, var_cible:str, var_cible_pos:tuple, indice_de_decoupage:int) -> float:
    """Test du khi deux"""

    groupeGauche, groupeDroite = groupe[indice_de_decoupage:], groupe[:indice_de_decoupage]

    khi_2 = 0
    
    l_khi2 = []
    for pos in var_cible_pos:

        G = sum([1 for groupe in groupeGauche if groupe[var_cible] == pos])
        D = sum([1 for groupe in groupeDroite if groupe[var_cible] == pos])

        l_khi2.append(G)
        l_khi2.append(D)

    total = len(groupe)
    total_G = len(groupeGauche)
    total_D = len(groupeDroite)
    total_non_spam = l_khi2[0] + l_khi2[1]
    total_spam = l_khi2[2] + l_khi2[3]

    G_non_spam = l_khi2[0]
    D_non_spam = l_khi2[1]
    G_spam = l_khi2[2]
    D_spam = l_khi2[3]

    theorique_G_non_spam = total_non_spam*total_G/total
    theorique_D_non_spam = total_non_spam*total_D/total
    theorique_G_spam = total_spam*total_G/total
    theorique_D_spam = total_spam*total_D/total

    if theorique_G_non_spam != 0:
        khi_2 += (G_non_spam - theorique_G_non_spam)**2 / theorique_G_non_spam
    if theorique_D_non_spam != 0:
        khi_2 += (D_non_spam - theorique_D_non_spam)**2 / theorique_D_non_spam
    if theorique_G_spam != 0:
        khi_2 += (G_spam - theorique_G_spam)**2 / theorique_G_spam
    if theorique_D_spam != 0:
        khi_2 += (D_spam - theorique_D_spam)**2 / theorique_D_spam

    if khi_2 < 3.841:
        return 0
    return khi_2
