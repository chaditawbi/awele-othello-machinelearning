#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def isInputInt(input1):
	try:
		int(input1)

		return True

	except ValueError:
		return False


def saisieCoup(jeu):
	""" jeu -> coup
		Retourne un coup a jouer
	"""
	game.affiche(jeu)

	coupsValides = game.getCoupsValides(jeu)
	print()
	print("Liste des coups jouables: ")
	for i in range(len(coupsValides)):
		print(str(i) + " => " + str(coupsValides[i]))
	
	selectedCoup = input("Choississez un numéro entre 0 et "+str(len(coupsValides)-1)+": ")
	if isInputInt(selectedCoup):
		selectedCoup = int(selectedCoup)
		if selectedCoup >= 0 and selectedCoup < len(coupsValides) and coupsValides[selectedCoup] in coupsValides:
			return coupsValides[selectedCoup]
		else:
			saisieCoup(jeu)
	else:
		saisieCoup(jeu)