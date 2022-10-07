#!/usr/bin/env python
# -*- coding: utf-8 -*-
import othello
import sys
sys.path.append("..")
import game
import pickle
import os
import textwrap
import random
game.game=othello
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire
import joueur_alphabeta
import joueur_horizon1
import numpy as np

def apprentissageSupervise(nbMax=1000):
    """Apprentissage supervisé avec horizon 1 et alphabeta horizon 5 à l'aide d'Oracle"""

    alpha = 1
    oracle=joueur_alphabeta
    apprenti=joueur_horizon1
    adversaire = joueur_alphabeta
    game.joueur1 = apprenti
    game.joueur2 = adversaire
    apprenti.poids=[2,8,-6,4,-5]
    horizonOracle = 3
    oracle.horizon=horizonOracle
    nombreDeDesaccord=0
    listeNbAccord=[]
    i = 0
    cpt=0
    coupJouesApprenti=0 # nombre de fois que l'apprenti a joué un coup
    while alpha > 0 and nbMax>cpt:
        i=0
        jeu=game.initialiseJeu()
        joueur_alphabeta.joueur=game.getJoueur(jeu)
        joueur_horizon1.joueur=game.getJoueur(jeu)

        while not game.finJeu(jeu):
            if i<4:
                coup=joueur_aleatoire.saisieCoup(jeu)
                i+=1
                game.joueCoup(jeu,coup)

            else :
                coupJouesApprenti=coupJouesApprenti+1
                listeCoupsValides = game.getCoupsValides(jeu)
                joueurOracleEstimation = []
                joueurApprentiEstimation = []
                joueurOracleParametres = []
                joueurApprentiParametres = []

                for coup in listeCoupsValides:
                    joueurOracleEstimation.append(oracle.estimation(jeu,coup, horizonOracle))
                    joueurOracleParametres.append(oracle.param1)
                    joueurApprentiEstimation.append(apprenti.estimation(jeu,coup))
                    joueurApprentiParametres.append(apprenti.param1)

                indiceMeilleurCoupOracle = np.argmax(joueurOracleEstimation)
                indiceMeilleurCoupApprenti = np.argmax(joueurApprentiEstimation)

                if not (indiceMeilleurCoupOracle == indiceMeilleurCoupApprenti):
                    for j in range(len(listeCoupsValides)):
                        evalOptimalApprenti = joueurApprentiEstimation[indiceMeilleurCoupOracle]
                        for k in range(len(joueurApprentiEstimation)):
                            if evalOptimalApprenti-joueurApprentiEstimation[k]<1:
                                for l in range(len(oracle.poids)):
                                    apprenti.poids[l] = apprenti.poids[l]-alpha * (joueurApprentiParametres[j][l]-joueurOracleParametres[j][l])
                
                    nombreDeDesaccord=nombreDeDesaccord+1 #Augmente un par un en cas différent indice de apprenti et oracle

                game.joueCoup(jeu,listeCoupsValides[indiceMeilleurCoupOracle])
                if(game.finJeu(jeu)):
                    num = game.getGagnant(jeu)
                    print("Le gagnant est: "+str(num))
                    break
                game.joueCoup(jeu,adversaire.saisieCoup(jeu))
        cpt+=1
        
        alpha=alpha*0.99999
        nbAccord=coupJouesApprenti-nombreDeDesaccord
        listeNbAccord.append((nbAccord/coupJouesApprenti)*100)
        coupJouesApprenti=0
        nombreDeDesaccord=0

random.seed()   
apprentissageSupervise(100) # 100 parties à jouer