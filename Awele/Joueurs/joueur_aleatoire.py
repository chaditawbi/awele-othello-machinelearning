#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

import random


temp = 0

def saisieCoup(jeu):
	global temp
	""" jeu -> coup
		Retourne un coup a jouer
	"""
	coupsValides = game.getCoupsValides(jeu)
	#print("Liste des coups jouables: "+str(coupsValides))
	if temp <= 4:
		temp += 1
		return random.choice(coupsValides)
	else:
		return decision(jeu, coupsValides)

def decision(jeu, lstCoupsValides):
	bestScore = -1000
	meilleurCoup = []

	for i in range(len(lstCoupsValides)):
		currCoup = lstCoupsValides[i]

		scoreGained = estimation(jeu, currCoup)

		if scoreGained >= bestScore:
			meilleurCoup = currCoup


	return meilleurCoup

def estimation(jeu, coup):
	jeuCpy = game.getCopieJeu(jeu)

	currEval = evaluation(jeuCpy, coup)


	game.joueCoup(jeuCpy, coup)


	finalEval = evaluation(jeuCpy, coup)

	return currEval + finalEval


def scoreDiff(jeu):
	scores = game.getScores(jeu)
	return scores[1] - scores[0]

def evaluation(jeu, coup):
	diffScores = scoreDiff(jeu)

	return diffScores

