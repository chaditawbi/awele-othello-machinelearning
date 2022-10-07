#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

import sys
sys.path.append("..")
import game

tailleX = 2 #Normalement fix forcé à 2
tailleY = 6

def initialiseJeu():
	"""Jeu Awele"""

	#Init plateau
	plateau = []

	#Lignes
	for i in range(tailleX):
		plateau.append([])

		#Colonnes
		for k in range(tailleY):
			plateau[i].append(4)


	return [plateau, 1, None, [], (0,0)]

def getNextCase(case, antiHoraire=True):
	if antiHoraire:
		if case[0] == 0 and case[1] >= (tailleY - 1):
			case = (1, (tailleY - 1))
		elif case[0] == 1 and case[1] <= 0:
			case = (0, 0)
		elif case[0] == 1:
			case = (case[0], case[1]-1) 
		else:
			case = (case[0], case[1]+1) 
	else:
		if case[0] == 0 and case[1] <= 0:
			case = (1, 0)
		elif case[0] == 1 and case[1] >= (tailleY - 1):
			case = (0, (tailleY - 1))	
		elif case[0] == 1:
			case = (case[0], case[1]+1) 
		else:
			case = (case[0], case[1]-1)   

	return case

def joueCoup(jeu, coup):
	#Egrainer
	graines = jeu[0][coup[0]][coup[1]]  #Récupère le nombre de graines à semer

	jeu[0][coup[0]][coup[1]] = 0 #Mise à zéro de la case en de départ

	currentCoup = coup #Handler sur le coup suivant/courant

	eatenCases = []

	while graines > 0:
		currentCoup = getNextCase(currentCoup, False) #Get Next Case

		if currentCoup != coup:
			jeu[0][currentCoup[0]][currentCoup[1]] += 1 #Ajout d'une graine
			graines -= 1 #On a déposé une graine sur une case donc -1

			eatenCases.append(currentCoup)

	copieJeu = game.getCopieJeu(jeu)

	#Manger
	scorePlayer = 0
	for i in range(len(eatenCases)): #Reverse parcours
		if eatenCases[-i-1][0] != coup[0] and (jeu[0][eatenCases[-i-1][0]][eatenCases[-i-1][1]] == 2 or jeu[0][eatenCases[-i-1][0]][eatenCases[-i-1][1]] == 3):
			scorePlayer += jeu[0][eatenCases[-i-1][0]][eatenCases[-i-1][1]]

			jeu[0][eatenCases[-i-1][0]][eatenCases[-i-1][1]] = 0
		else:
			break


	#Si joueur adverse affamé alors on reprend le jeu initial
	if estAffame(jeu, (jeu[1] % 2 + 1)):
		jeu = copieJeu
		jeu[2] = None
		return

	#Update score
	game.updateScores(jeu, scorePlayer, jeu[1])

	#Update coup joué
	jeu[3].append(coup)

	# Update coups Valides
	jeu[2] = None

	

	#Update joueur qui va jouer
	game.changeJoueur(jeu)


def estAffame(jeu, joueur):
	return sum(jeu[0][joueur - 1]) == 0

def estValide(jeu, coup, checkNourrit=False):
	if not (coup[0] == (jeu[1]-1)):
		return False

	g = jeu[0][coup[0]][coup[1]]

	if g == 0:
		return False

	if checkNourrit:
		if coup[0] == 0:
			return g > coup[1]
		if coup[0] == 1:
			return g > (5 - coup[1])

	return True

def listeCoupsValides(jeu):
	affame = estAffame(jeu, jeu[1] % 2 + 1)
	#print("Joueur: "+str(jeu[1])+" est Affamé:" + str(affame))

	return [(jeu[1] - 1, c) for c in range(6) if estValide(jeu, (jeu[1] - 1, c), affame)]


totalCoup = 0

def finJeu(jeu):
	global totalCoup
	totalCoup += 1
	#print("TotalCoup: "+str(totalCoup))
	return (len(listeCoupsValides(jeu)) == 0) or (totalCoup == 5000)

def finaliseJeu(jeu):
   """jeu->jeu
   Met à jour le score et retourne le jeu final
   """
   #Le score de joueur 1
   score1 = 0
   #Le score de joueur 2 
   score2 = 0
   
   # prend les sommes de toutes les cases pour rajouter aux scores respectifs
   for i in range(0,6):
      score1+=game.getCaseVal(jeu,0,i) 
   for i in range(0,6):
      score2+=game.getCaseVal(jeu,1,i)  
    
   # incrémentation du score
   jeu[4] = (score1, score2)
   
   return jeu
	
