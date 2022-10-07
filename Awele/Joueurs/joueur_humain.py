#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def isInputIsInt(input1, input2):
	try:
		selectedCoupX = int(input1)
		selectedCoupY = int(input2)

		return True

	except ValueError:
		return False


def saisieCoup(jeu):
	""" jeu -> coup
		Retourne un coup a jouer
	"""
	game.affiche(jeu)

	coupsValides = game.getCoupsValides(jeu)
	print("Liste des coups jouables: "+str(coupsValides))
	
	selectedCoupX = input("Choississez un coup X: ")
	selectedCoupY = input("Choississez un coup Y: ")

	while not isInputIsInt(selectedCoupX, selectedCoupY):
		print("Veuillez entrer des nombres correctes !")
		selectedCoupX = input("Choississez un coup X: ")
		selectedCoupY = input("Choississez un coup Y: ")

	selectedCoupX = int(selectedCoupX)
	selectedCoupY = int(selectedCoupY)

	selectedCoup = (selectedCoupX, selectedCoupY)

	while not selectedCoup in coupsValides:
		print("Coup non Valide, réessayer !")
		selectedCoupX = input("Choississez un coup X: ")
		selectedCoupY = input("Choississez un coup Y: ")

		while not isInputIsInt(selectedCoupX, selectedCoupY):
			print("Veuillez entrer des nombres correctes !")
			selectedCoupX = input("Choississez un coup X: ")
			selectedCoupY = input("Choississez un coup Y: ")

		selectedCoupX = int(selectedCoupX)
		selectedCoupY = int(selectedCoupY)

		selectedCoup = (selectedCoupX, selectedCoupY)

	return selectedCoup
