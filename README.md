# PUISSANCE 4 PVE

## Description

Bienvenue dans le jeu de Puissance 4 implémenté en Python. Dans cette version, vous jouez contre l'ordinateur : l'utilisateur doit aligner 4 jetons avant que l'ordinateur ne le fasse.

## Installation

1. Assurez-vous d'avoir Python installé sur votre machine.

2. Installez la bibliothèque colorama avec la commande suivante :

    ```bash
    pip install colorama
    ```

3. Lancez l'application :

    ```bash
    python main.py
    ```

## Comportement de l'IA (ordinateur)

À chaque tour de jeu, l'IA vérifie pour chaque colonne de la grille, dans cet ordre :

1. Si jouer dans cette colonne lui donne 4 jetons alignés, elle joue directement dans cette colonne.

2. Si, au prochain tour, l'utilisateur jouait dans cette colonne et obtenait 4 jetons alignés, l'IA joue cette colonne pour le contrer.

3. Sinon, elle vérifie pour chaque colonne si le fait de jouer un jeton lui donne 3 jetons alignés. Elle vérifie également s'il y a assez d'espace pour aligner 4 jetons. Si ces deux conditions sont réunies, elle sauvegarde cette colonne dans une liste.

4. Même chose que pour le point 3, mais avec 2 jetons alignés.

5. Une fois que chaque colonne est vérifiée, l'IA sélectionne aléatoirement une colonne dans la liste qui stocke les colonnes avec 3 jetons alignés et la joue.

6. Si cette première liste est vide, elle sélectionne aléatoirement une colonne dans la liste qui stocke les colonnes avec 2 jetons alignés et la joue.

7. Si encore une fois la liste est vide, elle choisit aléatoirement une colonne parmi toutes les colonnes qui ne sont pas déjà pleines.
