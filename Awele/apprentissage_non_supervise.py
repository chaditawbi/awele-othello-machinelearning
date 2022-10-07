#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

import random
import os

import game
import awele
game.game=awele
sys.path.append("./Joueurs")
import joueur_humain
import joueur_aleatoire
import joueur_minimax
import joueur_alphabeta
import joueur_horizon1

def partie(affichage=False, alea=True, nbMax=1000):
    """Joue une partie pendant nbMax itérations"""
    i=0
    jeu=game.initialiseJeu()
    while not game.finJeu(jeu):
        if alea and i<4:
            coup=joueur_aleatoire.saisieCoup(jeu)
        else:
            coup=game.saisieCoup(jeu)
        if i > nbMax: 
            return
        if affichage:
            game.affiche(jeu)
            
        game.joueCoup(jeu,coup)
        i+=1
    jeu = awele.finaliseJeu(jeu)
    return game.getGagnant(jeu)

def stats(nbParties,joueur):
    """Stats d'un joueur"""
    nbGagne = 0
    nbNul = 0
    for i in range(nbParties):
        gagnant = partie()
        if gagnant == joueur:
            nbGagne+=1
        if gagnant == 0:
            nbNul+=1
    return (nbParties, nbGagne, nbNul)

def afficheStats(resStats):
    """Score de la partie"""
    nbPerdu = resStats[0]-resStats[1]-resStats[2]
    print("Nombre de parties gagnées : {1}/{0}\n\
Nombre de parties nulles : {2}/{0}\n\
Nombre de parties perdues : {3}/{0}".format(resStats[0],resStats[1],resStats[2], nbPerdu))



def apprentissageNonSupervise(nbMax = 100):
    """Apprentissage non supervisé avec horizon 1 en premier joueur et alphabeta ou minimax horizon 3 à l'aide du joueur Oracle"""
    cpt = 0 # nb explo
    epsilon = 1 # init point opti
    nbParties = 20 # nb parties sur les poids
    tauxVictoire = 0 # initialisation du score d'un test des poids
    game.joueur1=joueur_horizon1
    game.joueur2=joueur_alphabeta

    # Initialisation des poids
    game.joueur1.poids = [2,-1,-1]
    game.joueur2.poids = [2,-1,-1]

    # Choix de l'horizon
    game.joueur2.horizon=3

    # initialisation de liste de score de test de poids
    listeTauxVictoire=[]

    # tant que l'exploration n'est pas achevée ou le score est inférieur à 100%
    while epsilon>0 and tauxVictoire<100 and cpt<nbMax:
        epsilon=epsilon*0.99999999
        i = random.randrange(0,len(game.joueur1.poids))
        # i : le paramètre modifié
        s = random.randrange(-1,1,2)
        # s : choix entre 1 et -1 (changer ou pas signe du paramètre)
        game.joueur1.poids[i] = game.joueur1.poids[i]*s*epsilon # exploration simple
        
        # statistiques pour quand joueur1 est le premier joueur
        stats1 = stats(nbParties,1)
        
        # stats pour quand joueur1 est le deuxième joueur
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp
        stats2 = stats(nbParties,2)
        
        nouvTauxVictoire = (stats1[1] + stats2[1])/(2*nbParties)*100 # moyenne des stats des deux études
        
        # On remets les joueurs à l'état de base
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp

        # si le nouveau taux de victoire est mieux, on ajoute le score à la liste des performances
        if nouvTauxVictoire > tauxVictoire:
            tauxVictoire = nouvTauxVictoire
            #print(game.joueur1.poids)
            print("En tant que premier joueur :")
            afficheStats(stats1)
            print("En tant que deuxième joueur :")
            afficheStats(stats2)
            listeTauxVictoire.append(nouvTauxVictoire)

        cpt+=1

random.seed()
apprentissageNonSupervise(100) # 100 parties