import random
from colorama import Fore, Style

NOMBRE_JETONS_POUR_VICTOIRE = 4

JETON_JOUEUR = f"{Fore.RED}X{Style.RESET_ALL}"
JETON_ORDI = f"{Fore.BLUE}O{Style.RESET_ALL}"
NB_LIGNES = 6
NB_COLONNES = 7

GRILLE = []


def afficher_titre_jeu():
    print('''
  _____  _    _ _____  _____ _____         _   _  _____ ______   _  _   
 |  __ \| |  | |_   _|/ ____/ ____|  /\   | \ | |/ ____|  ____| | || |  
 | |__) | |  | | | | | (___| (___   /  \  |  \| | |    | |__    | || |_ 
 |  ___/| |  | | | |  \___ \\\\___ \ / /\ \ | . ` | |    |  __|   |__   _|
 | |    | |__| |_| |_ ____) |___) / ____ \| |\  | |____| |____     | |  
 |_|     \____/|_____|_____/_____/_/    \_\_| \_|\_____|______|    |_|  
''' ) 


def intialiser_grille():
    for i in range(NB_LIGNES):
        ligne = []
        GRILLE.append(ligne)
        for j in range(NB_COLONNES):
            ligne.append(" ")


def afficher_grille():
    print("     1   2   3   4   5   6   7")
    for indice, ligne in enumerate(GRILLE):
        print("   +---+---+---+---+---+---+---+")
        print(f" {indice + 1} ", end='')
        for element in ligne:
            print(f"| {element} ", end='')
        print(f"| {indice + 1}\n", end='')
    print("   +---+---+---+---+---+---+---+")
    print("     1   2   3   4   5   6   7")


def colonne_est_pleine(colonne):
    indice_colonne = colonne-1
    if GRILLE[0][indice_colonne] != ' ':
        return True
    return False


def demander_choix_colonne_utilisateur():
    choix_colonne_utilisateur = 0
    while choix_colonne_utilisateur not in (range(1, 8)):
        choix_colonne_utilisateur = input("Rentrez le numéro de la colonne dans la quelle vous souhaitez jouer :")
        try :
            choix_colonne_utilisateur = int(choix_colonne_utilisateur)
            if choix_colonne_utilisateur not in range(1, 8):
                print("Le numéro de colonne ne peut être compris qu'entre 1 et 7 !")
                return demander_choix_colonne_utilisateur()
        except:
            print("Il faut rentrer un nombre !")
            return demander_choix_colonne_utilisateur()
        if colonne_est_pleine(choix_colonne_utilisateur):
            print("Cette colonne est pleine ! ")
            return demander_choix_colonne_utilisateur()
        return choix_colonne_utilisateur


def jouer_coup(colonne, jeton):
    indice_colonne = colonne - 1
    for indice, ligne in enumerate(GRILLE[::-1]):
        if ligne[indice_colonne] == ' ':
            ligne[indice_colonne] = jeton
            position_jeton = (colonne, NB_LIGNES - indice)
            break
    return position_jeton


def recuprer_position_jeton_potentielle(colonne):
    for indice, ligne in enumerate(GRILLE[::-1]):
        if ligne[colonne-1] == ' ':
            position_jeton = (colonne, NB_LIGNES - indice)
            break
    return position_jeton


def grille_est_pleine():
    for colonne in GRILLE[0]:
        if colonne == ' ':
            return False
    return True


def case_est_dans_grille(indice_colonne, indice_ligne):
    if 0 <= indice_ligne < NB_LIGNES and 0 <= indice_colonne < NB_COLONNES:
        return True
    return False


def recuperer_liste_colonnes_jouables():
    liste_colonnes_valides = []
    for i in range(NB_COLONNES):
        if GRILLE[0][i] == ' ':
            liste_colonnes_valides.append(i+1)
    return liste_colonnes_valides


def nb_jeton_direction(position_jeton, deplacement_horizontal, deplacement_vertical, jeton):
    compteur = 1

    indice_ligne = position_jeton[1] - 1
    indice_colonne = position_jeton[0] - 1

    while case_est_dans_grille(indice_colonne + deplacement_horizontal, indice_ligne + deplacement_vertical) and GRILLE[indice_ligne + deplacement_vertical][indice_colonne + deplacement_horizontal] == jeton: 
        indice_ligne += deplacement_vertical
        indice_colonne += deplacement_horizontal
        compteur +=1
            
    return compteur


def axe_jetons_alignes(position_jeton, jeton, nombre_jetons_alignes_a_evaluer):
    deplacements_axe_NE_SO = ((1,1),(-1,-1))
    deplacements_axe_NO_SE = ((1,-1), (-1,1))
    deplacements_axe_E_O = ((1,0), (-1,0))
    deplacements_axe_N_S = ((0,1),(0,-1))

    nb_jetons_axe_NE_SO = (nb_jeton_direction(position_jeton, 1, 1,jeton) + nb_jeton_direction(position_jeton,-1,-1,jeton))-1
    nb_jetons_axe_NO_SE = (nb_jeton_direction(position_jeton,1,-1,jeton) + nb_jeton_direction(position_jeton,-1,1,jeton))-1
    nb_jetons_axe_E_O = (nb_jeton_direction(position_jeton,1,0,jeton) + nb_jeton_direction(position_jeton,-1,0,jeton))-1
    nb_jetons_axe_N_S = (nb_jeton_direction(position_jeton,0,1,jeton) + nb_jeton_direction(position_jeton,0,-1,jeton))-1

    nb_jeton_max = max(nb_jetons_axe_NE_SO, nb_jetons_axe_NO_SE, nb_jetons_axe_E_O, nb_jetons_axe_N_S)

    if nb_jeton_max >= nombre_jetons_alignes_a_evaluer:
        if nb_jeton_max == nb_jetons_axe_NE_SO:
            return deplacements_axe_NE_SO
        elif nb_jeton_max == nb_jetons_axe_NO_SE:
            return deplacements_axe_NO_SE
        elif nb_jeton_max == nb_jetons_axe_E_O:
            return deplacements_axe_E_O
        elif nb_jeton_max == nb_jetons_axe_N_S:
            return deplacements_axe_N_S
    else:
        return None
    

def nb_jeton_et_cases_vide_direction(position_jeton, deplacement_horizontal, deplacement_vertical, jeton):
    compteur = 1
    cases_valides = (jeton, ' ')
    indice_ligne = position_jeton[1] - 1
    indice_colonne = position_jeton[0] - 1

    while case_est_dans_grille(indice_colonne + deplacement_horizontal, indice_ligne + deplacement_vertical) and GRILLE[indice_ligne + deplacement_vertical][indice_colonne + deplacement_horizontal] in cases_valides: 
        indice_ligne += deplacement_vertical
        indice_colonne += deplacement_horizontal
        compteur +=1
            
    return compteur


def place_suffisante_pour_alignement_victoire(deplacements_axe, jeton, postion_jeton):
    deplacement_horizontal1 = deplacements_axe[0][0]
    deplacement_vertical1 = deplacements_axe[0][1]
    deplacement_horizontal2 = deplacements_axe[1][0]
    deplacement_vertical2 = deplacements_axe[1][1]

    nombre_cases_vides_ou_avec_jeton = (nb_jeton_et_cases_vide_direction(postion_jeton, deplacement_horizontal1,deplacement_vertical1, jeton) + nb_jeton_et_cases_vide_direction(postion_jeton, deplacement_horizontal2,deplacement_vertical2, jeton)) - 1
    if nombre_cases_vides_ou_avec_jeton >= NOMBRE_JETONS_POUR_VICTOIRE:
        return True
    return False


def recuperer_choix_colonne_ordinateur():
    colonne_victoire_ou_contre = 0
    colonnes_donnant_3_jetons_alignes = []
    colonnes_donnant_2_jetons_alignes = []
    
    for i in range(NB_COLONNES):
        colonne = i+1
        if colonne_est_pleine(colonne):
            continue
        position_jeton_potentiel = recuprer_position_jeton_potentielle(colonne)
        if axe_jetons_alignes(position_jeton_potentiel, JETON_ORDI, NOMBRE_JETONS_POUR_VICTOIRE):
            colonne_victoire_ou_contre = colonne
            break
        elif axe_jetons_alignes(position_jeton_potentiel, JETON_JOUEUR, NOMBRE_JETONS_POUR_VICTOIRE):
            colonne_victoire_ou_contre = colonne

        elif axe_jetons_alignes(position_jeton_potentiel, JETON_ORDI, 3):
            deplacement_axe = axe_jetons_alignes(position_jeton_potentiel, JETON_ORDI, 3)
            if place_suffisante_pour_alignement_victoire(deplacement_axe, JETON_ORDI, position_jeton_potentiel):
                colonnes_donnant_3_jetons_alignes.append(colonne)

        elif axe_jetons_alignes(position_jeton_potentiel, JETON_ORDI, 2):
            deplacement_axe = axe_jetons_alignes(position_jeton_potentiel, JETON_ORDI, 2)
            if place_suffisante_pour_alignement_victoire(deplacement_axe, JETON_ORDI, position_jeton_potentiel):
                colonnes_donnant_2_jetons_alignes.append(colonne)

    if colonne_victoire_ou_contre:
        meilleure_colonne = colonne_victoire_ou_contre
        print("Contre ou victoire")
    elif colonnes_donnant_3_jetons_alignes:
        meilleure_colonne = random.choice(colonnes_donnant_3_jetons_alignes)
        print("choix 3 jetons")
    elif colonnes_donnant_2_jetons_alignes:
        meilleure_colonne = random.choice(colonnes_donnant_2_jetons_alignes)
        print("choix 2 jetons")
    else:
        meilleure_colonne = random.choice(recuperer_liste_colonnes_jouables())
        print("choix random")

    return meilleure_colonne

# ------------------------ JEU ------------------------ #


afficher_titre_jeu()
intialiser_grille()

while True:
    afficher_grille()
    choix_colonne_utilisateur = demander_choix_colonne_utilisateur()
    postion_jeton_joueur = jouer_coup(choix_colonne_utilisateur, JETON_JOUEUR)

    if axe_jetons_alignes(postion_jeton_joueur, JETON_JOUEUR, NOMBRE_JETONS_POUR_VICTOIRE):
        afficher_grille()
        print("VICTOIRE ! ")
        break

    if grille_est_pleine():
        print("EGALITE !")
        break
    
    choix_colonne_ordinateur = recuperer_choix_colonne_ordinateur()
    position_jeton_ordinateur = jouer_coup(choix_colonne_ordinateur, JETON_ORDI)

    if axe_jetons_alignes(position_jeton_ordinateur, JETON_ORDI, NOMBRE_JETONS_POUR_VICTOIRE):
        afficher_grille()
        print("DEFAITE ! ")
        break

    if grille_est_pleine():
        print("EGALITE !")
        break
