#!/usr/bin/env python
# -*- coding: utf-8 -*-

# plateau: List[List[nat]]
# liste de listes (lignes du plateau) d'entiers correspondant aux contenus des cases du plateau de jeu

# coup:[nat nat]
# Numero de ligne et numero de colonne de la case correspondante a un coup d'un joueur

# Jeu
# jeu:[plateau nat List[coup] List[coup] List[nat nat]]
# Structure de jeu comportant :
#           - le plateau de jeu
#           - Le joueur a qui c'est le tour de jouer (1 ou 2)
#           - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#           - La liste des coups joues jusqu'a present dans le jeu
#           - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2

import copy
import time

game=None #Contient le module du jeu specifique: awele ou othello
joueur1=None #Contient le module du joueur 1
joueur2=None #Contient le module du joueur 2


#Fonctions minimales 

def getCopieJeu(jeu):
	""" jeu->jeu
		Retourne une copie du jeu passe en parametre
		Quand on copie un jeu on en calcule forcement les coups valides avant
	"""
	return [copy.deepcopy(jeu[0]), jeu[1], getCoupsValides(jeu), copy.deepcopy(jeu[3]), copy.deepcopy(jeu[4])] 


def finJeu(jeu):
	""" jeu -> bool
		Retourne vrai si c'est la fin du jeu
	"""
	return game.finJeu(jeu)

def saisieCoup(jeu):
	""" jeu -> coup
		Retourne un coup a jouer
		On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
		et qu'elle retourne obligatoirement un coup valide
	"""
	gameCopy = getCopieJeu(jeu)
	joueur = joueur1
	if gameCopy[1] == 2:
		joueur = joueur2
	coup = joueur.saisieCoup(gameCopy)
	#print(coup)
	while not coupValide(gameCopy, coup):
		#print("Coup non valide")
		coup = joueur.saisieCoup(gameCopy)
		#print("Coup: "+str(coup))
		time.sleep(2)

	return coup

def getCoupsValides(jeu):
	""" jeu  -> List[coup]
		Retourne la liste des coups valides dans le jeu passe en parametre
		Si None, alors on met a jour la liste des coups valides
	"""
	#print("Jeu 2 coups valide est:"+str(jeu[2]))
	if jeu[2] is None:
		jeu[2] = game.listeCoupsValides(jeu)
	return jeu[2]

def coupValide(jeu,coup):
	"""jeu*coup->bool
		Retourne vrai si le coup appartient a la liste de coups valides du jeu
	"""
	return coup in getCoupsValides(jeu)

def joueCoup(jeu,coup):
	"""jeu*coup->void
		Definition: Joue un coup a l'aide de la fonction joueCoup defini dans le module game
		Hypothese:le coup est valide
		Met tous les champs de jeu à jour (sauf coups valides qui est fixée à None)
	"""
	game.joueCoup(jeu, coup)


def initialiseJeu():
	""" void -> jeu
		Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
	"""
	return game.initialiseJeu()

def getGagnant(jeu):
	"""jeu->nat
	Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
	"""
	if jeu[4][0] > jeu[4][1]:
		return 1
	elif jeu[4][0] < jeu[4][1]:
		return 2
	else:
		return 0

def affiche(jeu):
	""" jeu->void
		Affiche l'etat du jeu de la maniere suivante :
				 Coup joue = <dernier coup>
				 Scores = <score 1>, <score 2>
				 Plateau :

						 |       0     |     1       |      2     |      ...
					------------------------------------------------
					  0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
					------------------------------------------------
					  1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
					------------------------------------------------
					...       ...          ...            ...
				 Joueur <joueur>, a vous de jouer
					
		 Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
	"""
	listeCoupsJoues = getCoupsJoues(jeu)
	print("Coup joue = " + (str(listeCoupsJoues)))

	nbLignes = len(getPlateau(jeu))
	nbColonnes = len(getPlateau(jeu)[0])

	print("Scores = " + str(getScore(jeu, 1)) + " , " + str(getScore(jeu, 2)))
	print("Plateau ("+str(nbLignes)+", "+str(nbColonnes)+"): ")

	beginStr = "    "
	beginLength = len(beginStr)

	clearArea()

	#N° Colonnes
	print(beginStr, end="")

	for k in range(0, nbColonnes):
			print(" | " + str(k), end="")
	print(" | ")

	for x in range(0, nbLignes):
		generatePrint(nbColonnes, beginLength)

		print("  " + str(x)+"  | ", end="")

		for k in range(0, nbColonnes):
			print(str(getCaseVal(jeu,x,k))+ " | ", end="")
		print()

	generatePrint(nbColonnes, beginLength)


	clearArea()

	print("Joueur "+ str(jeu[1]) +", a vous de jouer")


def generatePrint(length, beginLength):
	for w in range(beginLength):
		print("-",end="")

	for x in range(length):
		for w in range(beginLength):
			print("-",end="")

	print("-",end="")
	print("-",end="")

	print()

def clearArea():
	for x in range(0,2):
		print()	



# Fonctions utiles

def getPlateau(jeu):
	""" jeu  -> plateau
		Retourne le plateau du jeu passe en parametre
	"""
	return jeu[0]

def getCoupsJoues(jeu):
	""" jeu  -> List[coup]
		Retourne la liste des coups joues dans le jeu passe en parametre
	"""
	return jeu[3]


def getScores(jeu):
	""" jeu  -> Couple[nat nat]
		Retourne les scores du jeu passe en parametre
	"""
	return jeu[4]

def getJoueur(jeu):
	""" jeu  -> nat
		Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
	"""
	return jeu[1]


def changeJoueur(jeu):
	""" jeu  -> void
		Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
	"""
	jeu[1] = (jeu[1] % 2 + 1)

def getScore(jeu,joueur):
	""" jeu*nat->int
		Retourne le score du joueur
		Hypothese: le joueur est 1 ou 2
	"""
	if joueur == 1:
		return jeu[4][0]
	else:
		return jeu[4][1]

def getCaseVal(jeu, ligne, colonne):
	""" jeu*nat*nat -> nat
		Retourne le contenu de la case ligne,colonne du jeu
		Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
	"""

	return jeu[0][ligne][colonne]

def updateScores(jeu, scoreToAdd, joueur):
	score1, score2 = getScores(jeu)
	if joueur == 1:
		jeu[4] = (score1 + scoreToAdd, score2) 

	else:
		jeu[4] = (score1, score2 + scoreToAdd)
