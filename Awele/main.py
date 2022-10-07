#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import awele
import sys
sys.path.append("..")
import game
game.game=awele
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire
import joueur_minimax
import joueur_oracle
import joueur_horizon3

game.joueur1=joueur_aleatoire
game.joueur2=joueur_aleatoire


jeu = game.initialiseJeu()

#game.affiche(jeu)


def partie():
	jeu = game.initialiseJeu()

	while not game.finJeu(jeu):
		coup = game.saisieCoup(jeu)
		game.joueCoup(jeu, coup)
		game.affiche(jeu)

	game.affiche(jeu)
	
	return game.getGagnant(jeu)

print("Le gagnant est: " + str(partie()))
