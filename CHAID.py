from lib import *
def test_khi_2(groupe:list, var_cible:str, var_cible_pos:tuple, indice_de_decoupage:int) -> float:
    """Test du khi deux"""

    groupeGauche, groupeDroite = groupe[indice_de_decoupage:], groupe[:indice_de_decoupage]

    khi_2 = 0

    resultats = {}

    # peut-être pas optimal
    for pos in var_cible_pos:

        G = sum([1 for groupe in groupeGauche if groupe[var_cible] == pos])
        D = sum([1 for groupe in groupeDroite if groupe[var_cible] == pos])

        theorique = (G + D) / 2

        khi_2 += (G - theorique)**2 / theorique
        khi_2 += (D - theorique)**2 / theorique

    if khi_2 < 3.84:
        return 0
    return khi_2
