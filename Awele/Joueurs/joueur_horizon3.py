#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

import math

# Paramètres
horizon=3

def estimation(jeu,coup,horizon):
    """
    Implémentation de l'algorithme minimax
    """
    estim=[]
    listeCoupsVal = game.getCoupsValides(jeu)
    if horizon==0 or listeCoupsVal==[] :
        return evaluation(jeu)
    
    copie1=game.getCopieJeu(jeu)
    game.joueCoup(copie1,coup)
    if(game.finJeu(copie1)):
        if(joueur==game.getGagnant(copie1)):
            return 1000
        if(game.getGagnant(copie1)==3-joueur):
            return -1000
        if(game.getGagnant(copie1)==0):
            return -50
    if joueur==game.getJoueur(jeu): # si joueur ami
        for nouvCoup in listeCoupsVal:
            copie=game.getCopieJeu(jeu)
            game.joueCoup(copie,nouvCoup)
            #game.changeJoueur(copie)
            estim.append(estimation(copie,nouvCoup,horizon-1))
        val=max(estim)
        return val           
    
    else: # si joueur ennemi
        for nouvCoup in listeCoupsVal:
            copie=game.getCopieJeu(jeu)
            game.joueCoup(copie,nouvCoup)
            #game.changeJoueur(copie)
            estim.append(estimation(copie,nouvCoup,horizon-1))
        val=min(estim)       
        return val

def evaluation(jeu):
    """jeu->int
    Hypothèse : coup est valide (assuré dans saisieCoup)
    Évalue la qualité d'un coup
    """
    
    # différence de score
    diffScores = game.getScore(jeu,joueur)-game.getScore(jeu,3-joueur)

    # nombre de cases vides
    nbCasesVides=0
    for i in range(0,6):
        if (game.getCaseVal(jeu,joueur-1,i) == 0):
            nbCasesVides=nbCasesVides+1
    
    # nombre de cases vulnerables
    nbCasesVulnerables=0
    for i in range(0,6):
        if (game.getCaseVal(jeu,joueur-1,i) == 1 or game.getCaseVal(jeu,joueur-1,i) == 2):
            nbCasesVulnerables=nbCasesVulnerables+1
            
    return 2*diffScores - nbCasesVides - nbCasesVulnerables
    

def decision(jeu):
    #On fait la décision
    listeCoups = game.getCoupsValides(jeu)
    meilleurScore = -math.inf
    if game.getJoueur(jeu) == joueur:
        listeCoups.reverse()
    
    meilleurCoup = listeCoups[0]
    for coup in listeCoups:
        copie=game.getCopieJeu(jeu)
        game.joueCoup(copie,coup)
        scoreEval = estimation(copie,coup,horizon)
        if meilleurScore < scoreEval:
            meilleurCoup = coup
            meilleurScore = scoreEval
    return meilleurCoup

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global joueur # attention : ne pas nommer un paramètre de fonction "joueur" !
    joueur = game.getJoueur(jeu)
    meilleur_coup=decision(jeu)
    return meilleur_coup