def test_khi_2(groupe:list, var_cible:str, var_cible_pos:tuple, indice_de_decoupage:int) -> float:
    """Test du khi deux"""

    groupeA, groupeB = groupe[indice_de_decoupage:], groupe[:indice_de_decoupage]

    khi_2 = 0

    for caracteristique in groupeA:
        gauche, droite = sum((dico[caracteristique] for dico in groupeA)) + sum((dico[caracteristique] for dico in groupeB))

        theorique = (gauche + droite) / 2

        khi_2 += ( (gauche - theorique)**2 + (droite - theorique)**2 ) / 2

    return khi_2
