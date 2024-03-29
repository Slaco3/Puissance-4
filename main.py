import random
from colorama import Fore, Style
import os
import platform

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
\n\n''' ) 


def intialiser_grille():
    for i in range(NB_LIGNES):
        ligne = []
        GRILLE.append(ligne)
        for j in range(NB_COLONNES):
            ligne.append(" ")


def afficher_grille():
    print("                      1   2   3   4   5   6   7")
    for indice, ligne in enumerate(GRILLE):
        print("                    +---+---+---+---+---+---+---+")
        print(f"                  {indice + 1} ", end='')
        for element in ligne:
            print(f"| {element} ", end='')
        print(f"| {indice + 1}\n", end='')
    print("                    +---+---+---+---+---+---+---+")
    print("                   &   1   2   3   4   5   6   7\n\n")


def colonne_est_pleine(colonne):
    indice_colonne = colonne-1
    if GRILLE[0][indice_colonne] != ' ':
        return True
    return False


def demander_choix_colonne_utilisateur():
    choix_colonne_utilisateur = 0
    while choix_colonne_utilisateur not in (range(1, 8)):
        choix_colonne_utilisateur = input("Rentrez le numéro de la colonne dans laquelle vous souhaitez jouer : ")
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
    nb_jeton_direction = 1

    indice_ligne = position_jeton[1] - 1
    indice_colonne = position_jeton[0] - 1

    while case_est_dans_grille(indice_colonne + deplacement_horizontal, indice_ligne + deplacement_vertical) and GRILLE[indice_ligne + deplacement_vertical][indice_colonne + deplacement_horizontal] == jeton: 
        indice_ligne += deplacement_vertical
        indice_colonne += deplacement_horizontal
        nb_jeton_direction +=1
            
    return nb_jeton_direction


def nb_jetons_et_cases_vide_direction(position_jeton, deplacement_horizontal, deplacement_vertical, jeton):
    nb_jeton_et_cases_vide_direction = 1
    cases_valides = (jeton, ' ')
    indice_ligne = position_jeton[1] - 1
    indice_colonne = position_jeton[0] - 1

    while case_est_dans_grille(indice_colonne + deplacement_horizontal, indice_ligne + deplacement_vertical) and GRILLE[indice_ligne + deplacement_vertical][indice_colonne + deplacement_horizontal] in cases_valides: 
        indice_ligne += deplacement_vertical
        indice_colonne += deplacement_horizontal
        nb_jeton_et_cases_vide_direction +=1
            
    return nb_jeton_et_cases_vide_direction


def place_suffisante_pour_alignement_victoire(deplacements_axe, jeton, postion_jeton):
    deplacement_horizontal1 = deplacements_axe[0][0]
    deplacement_vertical1 = deplacements_axe[0][1]
    deplacement_horizontal2 = deplacements_axe[1][0]
    deplacement_vertical2 = deplacements_axe[1][1]

    nombre_cases_vides_ou_avec_bon_jeton = (nb_jetons_et_cases_vide_direction(postion_jeton, deplacement_horizontal1,deplacement_vertical1, jeton) + nb_jetons_et_cases_vide_direction(postion_jeton, deplacement_horizontal2,deplacement_vertical2, jeton)) - 1
    if nombre_cases_vides_ou_avec_bon_jeton >= NOMBRE_JETONS_POUR_VICTOIRE:
        return True
    return False


def position_jeton_donne_bon_nombre_jetons_alignes(position_jeton, jeton, nombre_jetons_alignes_a_evaluer):
    deplacements_axe_NE_SO = ((1,1),(-1,-1))
    deplacements_axe_NO_SE = ((1,-1), (-1,1))
    deplacements_axe_E_O = ((1,0), (-1,0))
    deplacements_axe_N_S = ((0,1),(0,-1))

    nb_jetons_axe_NE_SO = (nb_jeton_direction(position_jeton, 1, 1,jeton) + nb_jeton_direction(position_jeton,-1,-1,jeton))-1
    nb_jetons_axe_NO_SE = (nb_jeton_direction(position_jeton,1,-1,jeton) + nb_jeton_direction(position_jeton,-1,1,jeton))-1
    nb_jetons_axe_E_O = (nb_jeton_direction(position_jeton,1,0,jeton) + nb_jeton_direction(position_jeton,-1,0,jeton))-1
    nb_jetons_axe_N_S = (nb_jeton_direction(position_jeton,0,1,jeton) + nb_jeton_direction(position_jeton,0,-1,jeton))-1


    if nb_jetons_axe_NE_SO >= nombre_jetons_alignes_a_evaluer and place_suffisante_pour_alignement_victoire(deplacements_axe_NE_SO, jeton, position_jeton):
        return True
    elif nb_jetons_axe_NO_SE >= nombre_jetons_alignes_a_evaluer and place_suffisante_pour_alignement_victoire(deplacements_axe_NO_SE, jeton, position_jeton):
        return True
    elif nb_jetons_axe_E_O >= nombre_jetons_alignes_a_evaluer and place_suffisante_pour_alignement_victoire(deplacements_axe_E_O, jeton, position_jeton):
        return True
    elif nb_jetons_axe_N_S >= nombre_jetons_alignes_a_evaluer and place_suffisante_pour_alignement_victoire(deplacements_axe_N_S, jeton, position_jeton):
        return True
    return False
    

def recuperer_choix_colonne_ordinateur():
    colonne_victoire_ou_contre = 0
    colonnes_donnant_3_jetons_alignes = []
    colonnes_donnant_2_jetons_alignes = []
    
    for i in range(NB_COLONNES):
        colonne = i + 1
        if colonne_est_pleine(colonne):
            continue

        position_jeton_potentiel = recuprer_position_jeton_potentielle(colonne)

        if position_jeton_donne_bon_nombre_jetons_alignes(position_jeton_potentiel, JETON_ORDI, NOMBRE_JETONS_POUR_VICTOIRE):
            colonne_victoire_ou_contre = colonne
            break

        elif position_jeton_donne_bon_nombre_jetons_alignes(position_jeton_potentiel, JETON_JOUEUR, NOMBRE_JETONS_POUR_VICTOIRE):
            colonne_victoire_ou_contre = colonne

        elif position_jeton_donne_bon_nombre_jetons_alignes(position_jeton_potentiel, JETON_ORDI, 3):
            colonnes_donnant_3_jetons_alignes.append(colonne)

        elif position_jeton_donne_bon_nombre_jetons_alignes(position_jeton_potentiel, JETON_ORDI, 2):
            colonnes_donnant_2_jetons_alignes.append(colonne)

    # print("colonnes 3 jetons potentiels alignés", colonnes_donnant_3_jetons_alignes)
    # print("colonnes 2 jetons potentiels alignés", colonnes_donnant_2_jetons_alignes)

    if colonne_victoire_ou_contre:
        meilleure_colonne = colonne_victoire_ou_contre
        # print("Contre ou victoire")
    elif colonnes_donnant_3_jetons_alignes:
        meilleure_colonne = random.choice(colonnes_donnant_3_jetons_alignes)
        # print("choix 3 jetons")
    elif colonnes_donnant_2_jetons_alignes:
        meilleure_colonne = random.choice(colonnes_donnant_2_jetons_alignes)
        # print("choix 2 jetons")
    else:
        meilleure_colonne = random.choice(recuperer_liste_colonnes_jouables())
        # print("choix random")

    return meilleure_colonne


def premier_tour():
    afficher_titre_jeu()
    afficher_grille()

    choix_colonne_utilisateur = demander_choix_colonne_utilisateur()
    jouer_coup(choix_colonne_utilisateur, JETON_JOUEUR)

    if choix_colonne_utilisateur in ((1, 2, 3, 5, 6, 7)):
        choix_colonne_ordinateur = 4
    else:
        choix_colonne_ordinateur = random.choice((3, 5))

    jouer_coup(choix_colonne_ordinateur, JETON_ORDI)


def effacer_ecran():
    systeme_exploitation = platform.system().lower()
    if systeme_exploitation == "linux" or systeme_exploitation == "darwin":
        os.system("clear")

    elif systeme_exploitation == "windows":
        os.system("cls")

    else:
        pass

# ------------------------ JEU ------------------------ #



intialiser_grille()
premier_tour()
effacer_ecran()

while True:
    afficher_titre_jeu()
    afficher_grille()

    choix_colonne_utilisateur = demander_choix_colonne_utilisateur()
    postion_jeton_joueur = jouer_coup(choix_colonne_utilisateur, JETON_JOUEUR)

    if position_jeton_donne_bon_nombre_jetons_alignes(postion_jeton_joueur, JETON_JOUEUR, NOMBRE_JETONS_POUR_VICTOIRE):
        effacer_ecran()
        afficher_titre_jeu()
        afficher_grille()
        print("VICTOIRE ! ")
        break

    if grille_est_pleine():
        print("EGALITE !")
        break
    

    choix_colonne_ordinateur = recuperer_choix_colonne_ordinateur()
    position_jeton_ordinateur = jouer_coup(choix_colonne_ordinateur, JETON_ORDI)
    # print("position dernier jeton ordi (x,y): ", position_jeton_ordinateur)

    if position_jeton_donne_bon_nombre_jetons_alignes(position_jeton_ordinateur, JETON_ORDI, NOMBRE_JETONS_POUR_VICTOIRE):
        effacer_ecran()
        afficher_titre_jeu()
        afficher_grille()
        print("DEFAITE ! ")
        break

    if grille_est_pleine():
        print("EGALITE !")
        break


    effacer_ecran()
