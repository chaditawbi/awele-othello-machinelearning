# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

prof = 4
cpt = 0

def evaluation (jeu):
    #retourne un score d'evaluation

    return jeu[-1][moi - 1] - jeu[-1][adv - 1]


def estimation (jeu, coup, p):
    #retourne le score d'utilite pour un coup donne
    global cpt
    cpt += 1
    copie = game.getCopieJeu(jeu)
    game.joueCoup(copie, coup)
    if game.finJeu(copie):
        g = game.getGagnant(copie)
        if g == moi:
            return 100000000
        else:
            if g == 0:
                return -500
            else:
                return -100000000

    if p == prof:
        return evaluation(copie)
    
    if p < prof:
        coups = game.getCoupsValides(copie)
        max_min = estimation(copie, coups[0], p+1)
        for c in coups[1:]:
            s = estimation(copie, c, p+1)
            if p % 2 == 0 and s > max_min:
                max_min = s
            if p % 2 != 0 and s < max_min:
                max_min = s
        return max_min
    
    
def decision(jeu, coups):
    #retourne le meilleur  coup et son score
    maxi = estimation(jeu, coups[0], 1)
    max_coup = coups[0]
#    print "coup "+str(max_coup)+"="+str(maxi)
    for c in coups[1:]:
        s = estimation(jeu, c, 1)
        if s > maxi:
            maxi = s
            max_coup = c
#        print "coup "+str(c)+"="+str(s)
    return max_coup

def saisieCoup(jeu):
	global moi, adv
	moi = game.getJoueur(jeu)
	adv = moi % 2 + 1
	coup = decision(jeu, game.getCoupsValides(jeu))
	return coup
