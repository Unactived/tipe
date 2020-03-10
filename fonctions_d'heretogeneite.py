def indice_de_diversite_de_Gini(groupe:list, caracteristique:str, indice_de_decoupage:int)->float:
        """prend en argument un groupe d'éléments (liste de dictionnaires), une caractéristique (chaîne de caractère) et indice_de_decoupage; 
        divise la liste en deux groupes selon la valeur seuil de la caractéristique ; 
        renvoie la somme des valeurs de la fonction indice de diversité de Gini pour les deux groupes."""
        l = sorted(groupe, key=lambda variable: variable[caracteristique])
        
