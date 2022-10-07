#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

import sys
sys.path.append("..")
import game

tailleX = 8 #Normalement fix forcé à 8
tailleY = 8

#Pions des joueurs:
#Joueur 1 => 'O'
#Joueur 2 => 'X'
#See getplayerTile()

def initialiseJeu():
    """Jeu othello"""

    #Init plateau
    plateau = []

    #Lignes
    for i in range(tailleX):
        plateau.append([])
		#Colonnes
        for k in range(tailleY):
            plateau[i].append(' ')

    plateau[3][3] = 'O'
    plateau[4][4] = 'O'
    plateau[4][3] = 'X'
    plateau[3][4] = 'X'

    return [plateau, 1, None, [], (0,0)]

def joueCoup(jeu, coup):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    plateau = jeu[0]
    xstart, ystart = coup
    tile = getPlayerTile(jeu)

    tilesToChange = chercheCoupsValide(plateau, tile, xstart, ystart)

    if not tilesToChange:
        #Update coup joué
        jeu[3].append(coup)

        # Update coups Valides
        jeu[2] = None

        #Update joueur qui va jouer
        game.changeJoueur(jeu)

    plateau[xstart][ystart] = tile
    for x, y in tilesToChange:
        plateau[x][y] = tile

    #Update score
    game.updateScores(jeu, len(tilesToChange), jeu[1])

    #Update coup joué
    jeu[3].append(coup)

    # Update coups Valides
    jeu[2] = None


    #Update joueur qui va jouer
    game.changeJoueur(jeu)


def estSurPlateau(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= (tailleX - 1) and y >= 0 and y <= (tailleY - 1)

def chercheCoupsValide(plateau, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.

    if plateau[xstart][ystart] != ' ' or not estSurPlateau(xstart, ystart):
        return False

    plateau[xstart][ystart] = tile # temporarily set the tile on the board.


    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'


    tilesToChange = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart

        x += xdirection # first step in the direction
        y += ydirection # first step in the direction

        if estSurPlateau(x, y) and plateau[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.

            x += xdirection
            y += ydirection

            if not estSurPlateau(x, y):
                continue

            while plateau[x][y] == otherTile:
                x += xdirection
                y += ydirection

                if not estSurPlateau(x, y): # break out of while loop, then continue in for loop
                    break

            if not estSurPlateau(x, y):
                continue

            if plateau[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:

                    x -= xdirection
                    y -= ydirection

                    if x == xstart and y == ystart:
                        break

                    tilesToChange.append([x, y])

    plateau[xstart][ystart] = ' ' # restore the empty space

    if len(tilesToChange) == 0: # If no tiles were flipped, this is not a valid move.
        return False

    return tilesToChange

def getPlayerTile(jeu):
    if jeu[1] == 1:
        return 'O'
    else:
        return 'X'

def listeCoupsValides(jeu):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    plateau = jeu[0]
    playerTile = getPlayerTile(jeu)
    listeCoupsValidesTemp = []

    for x in range(tailleX):
        for y in range(tailleY):
            if chercheCoupsValide(plateau, playerTile, x, y):
                listeCoupsValidesTemp.append([x, y])

    return listeCoupsValidesTemp
    

def finJeu(jeu):
    plateau = jeu[0]

    found = False
    for i in range(tailleX):
        for k in range(tailleY):
            if plateau[i][k] == ' ':
                found = True
                break

    return not found or listeCoupsValides(jeu) == []
