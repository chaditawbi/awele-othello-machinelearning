#!/usr/bin/env python
# -*- coding: utf-8 -*-
import awele
import sys
sys.path.append("..")
import game
import random
game.game=awele
sys.path.append("./Joueurs")
import joueur_horizon1_apprentissage
game.joueur1=joueur_horizon1_apprentissage
game.joueur2=joueur_horizon1_apprentissage

#poids = [2,-1,-1]

def apprentissage():
    epsilon = 1
    resJeu = 10
    j = 0
    game.joueur1.poids = [2,-1, -1]
    #meilleursPoids = open('poids', 'w')
    while j<500:
        epsilon=epsilon*0.99
        i = random.randrange(0,len(game.joueur1.poids))
        # i : le paramètre modifié
        s = random.randrange(-1,1,2)
        # s : choix entre 1 et -1
        game.joueur1.poids[i] = game.joueur1.poids[i]*s*epsilon
        stats1 = stats(10,1)
        
        #On change la place  des joueurs,le joueur apprenti est dans la place 2
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp
        stats2 = stats(10,2)
        
        
        nouvResJeu = stats1[1] +  stats2[1]
        #nouvResJeu : tuple ResJeu: int
        
        #On reprend le joueur 1 pour apprenti
        tmp = game.joueur2
        game.joueur2 = game.joueur1
        game.joueur1 = tmp
        
        
        if nouvResJeu > resJeu:
            resJeu = nouvResJeu
            with open('poids.txt', 'a') as meilleursPoids:
                meilleursPoids.write(str(game.joueur1.poids)+"\n")
            print(game.joueur1.poids)
            print("En tant que premier joueur :")
            afficheStats(stats1)
            print("En tant que deuxième joueur :")
            afficheStats(stats2)
            
        if(resJeu==20):
            break
        j+=1
    rgs=regression(joueur1.evaluations,sum(evaluations)/len(evaluations)) #La régression des évaluations

def regression(listescore,somme):
    w=0
    for score in listescore:
        if((score-somme)<1):
            somme=score
        w=w+(score-somme)*(score-somme)
    
    return w

def ranking(e1,e2):
    return max(1-eval(e1)+eval(e2))

        
def afficheStats(resStats):
    nbPerdu = resStats[0]-resStats[1]-resStats[2]
    print("Nombre de parties gagnées : {1}/{0}\n\
Nombre de parties nulles : {2}/{0}\n\
Nombre de parties perdues : {3}/{0}".format(resStats[0],resStats[1],resStats[2], nbPerdu))

def stats(nbParties,joueur):
    """ int,int->int
    Retourne le nombre de parties gagnées
    """
    nbGagne = 0
    nbNul = 0
    for i in range(nbParties):
        gagnant = partie()
        if gagnant == joueur:
            nbGagne+=1
        if gagnant == 0:
            nbNul+=1
        print("Partie jouées : {}".format(i+1))
    return (nbParties, nbGagne, nbNul)

def partie(affichage=False, alea=True, nbMax=1000):
    """bool->int
        Boucle principale du jeu, choix d'afficher et de randomiser
        4 premiers tours. Retourne le joueur gagnant
    """
    i=0
    jeu=game.initialiseJeu()
    while not game.finJeu(jeu):
        if alea and i<4:
            coup=joueur_aleatoire.saisieCoup(jeu)
        else:
            coup=game.saisieCoup(jeu)
        if i > nbMax: 
            print("Erreur : atteint limite d'itérations")
            return
        if affichage:
            game.affiche(jeu)
            
        game.joueCoup(jeu,coup)
        i+=1
    jeu = awele.finaliseJeu(jeu) # faut peut-être mettre dans game.py
    #print("Joueur gagnant : {}".format(game.getGagnant(jeu)))
    return game.getGagnant(jeu)

random.seed()
#resStatsTest = stats(100,1)
#afficheStats(resStatsTest)
apprentissage()