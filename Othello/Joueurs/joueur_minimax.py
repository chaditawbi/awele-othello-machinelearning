#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

import math

# Paramètres
horizon=1

global poids
poids = [2,8,-6,4,-5]


def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global joueur
    joueur = game.getJoueur(jeu)
    meilleurCoup=decision(jeu)
    return meilleurCoup

def dot(v1,v2):
    """ Hypothèse : len(v1)==len(v2)
    """
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def estimation(jeu,coup,horizon):
    """
    Implémentation de l'algorithme minimax
    """
    copie=game.getCopieJeu(jeu)
    game.joueCoup(copie,coup)


    if(game.finJeu(copie)):
        if(joueur==game.getGagnant(copie)):
            return 100000
        if(game.getGagnant(copie)==3-joueur):
            return -100000
        if(game.getGagnant(copie)==0):
            return -50000

    if horizon==0:
        return evaluation(copie)
    
    listeCoupsVal = game.getCoupsValides(copie)
    
    if joueur==game.getJoueur(copie): # si joueur ami
        val=-math.inf
        for nouvCoup in listeCoupsVal:
            val=max(val,estimation(copie,nouvCoup,horizon-1))
        return val           
    
    else: # si joueur ennemi
        val=math.inf
        for nouvCoup in listeCoupsVal:
            val=min(val,estimation(copie,nouvCoup,horizon-1))      
        return val


def evaluation(jeu):
    """jeu,coup->int
    Hypothèse : coup est valide (assuré dans saisieCoup)
    Évalue la qualité d'un coup
    """
    #if(game.finJeu(jeu)):
    #    if(joueur==game.getGagnant(jeu)):
    #        return 100000
    #    if(game.getGagnant(jeu)==3-joueur):
    #        return -100000
    #    if(game.getGagnant(jeu)==0):
    #        return -50000
        

    param=[]
    coup = jeu[3][-1]

    #La différence de score
    diffScores = game.getScore(jeu,joueur)-game.getScore(jeu,3-joueur)
    param.append(diffScores)
    
    #Les coins
    Coins=[(0,0),(0,7),(7,0),(7,7)]
    c=0
    if coup in Coins:
        c=1
    param.append(c)
    
    #Zone de danger
    DangerZone1=[(1,0),(0,1),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6)]
    DangerZone2=[(6,7),(6,6),(7,6),(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6)]
    d=0
    if coup in DangerZone1 or DangerZone2:
        d=d+1
    param.append(d)
    
    #place safe
    PlaceSafe=[(0,2),(0,3),(0,4),(0,5),(7,2),(7,3),(7,4),(7,5),(2,0),(3,0),(4,0),(5,0)]
    ps=0
    if coup in PlaceSafe:
        ps=ps+1
    param.append(ps)
    
    nbrCasesVidesAutour=0
    for j in range(-1,1):
        for k in range(-1,1):
            if(coup[0]+j>0 or coup[0]+j<7 or coup[1]+k>0 or coup[1]+k<7 ):
                if(game.getCaseVal(jeu,coup[0]+j,coup[1]+k)==0):
                    nbrCasesVidesAutour=nbrCasesVidesAutour+1
    param.append(nbrCasesVidesAutour)
    
    return dot(poids,param)

    
def decision(jeu):
    #On fait la décision
    listeCoups = game.getCoupsValides(jeu)
    meilleurScore = -math.inf
    #if game.getJoueur(jeu) == joueur:
    #    listeCoups.reverse()
    
    meilleurCoup = listeCoups[0]
    for coup in listeCoups:
        scoreEval = estimation(jeu,coup,horizon)
        if meilleurScore < scoreEval:
            meilleurCoup = coup
            meilleurScore = scoreEval
    return meilleurCoup
