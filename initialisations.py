from random import *
import time
import pygame
def paquet():
    """
    Creer un paquet traditionel de 52 cartes (4 familles x 13 cartes)
    
    Renvoie un liste de ces cartes
    """
    c={0:"Carreau", 1:"Coeur", 2:"Pic", 3:"Trefle"}
    tetes={1:"Vallet", 2:"Dame", 3:"Roi"}
    l=[]
    for couleur in range(4):
        for i in range(1,11):
            if i == 1:
                l.append(str("As de"+" "+str(c[couleur])))
            else :
                l.append(str(str(i)+" de "+ str(c[couleur])))
        for i in range(1,4):
            l.append(str(str(tetes[i])+" de "+str(c[couleur])))
    return l

def ValeurCarte(c,j,dico_scores):
    """
    Renvoie la valeur d'une carte (ex: 5 de Pic = 5)
    """
    valeur= c.split()[0]
    res= valeur
    
    if valeur == "As":
        
        if j=='croupier' or (('bot' in j)==True):
            if dico_scores[j]>10:
                res = 1
            else:
                res = 11
        
        else:
            res = input(str(j)+", Vous avez tiré un AS, 1 ou 11? : ")
            while res !='1' and res !='11':
                res = input("1 ou 11 ???")
    
    elif valeur== "Vallet" or valeur=='Dame' or valeur=='Roi':
        res = 10

    return int(res)


def InitPioche(n):
    """
    Renvoie un liste de n paquet crees avec la fonction paquet() et les melange.
    """
    P=[]
    for i in range(n):
        P+=paquet()
    shuffle(P)
    return P

def Pioche(paquet,x=1):
    p=[]
    while len(p)<x:
        p.append(paquet[0])
        paquet.pop(0)
    return p


#-------------------------------------------------------------------------------------------#-------------------------------------------------------------------------------------------

def InitJoueurs(n,l=False):
    """
    Permet de faire une liste de joueurs/bots en demandant a l'utilisateur
    
    Renvoie cette liste et le niveau d'intelligence des bots (si il y'en a)
    """

    L=[]
    for i in range(n):
        L.append(input("prenom du joueur numero "+str(i+1)+": "))
    

    bot=int(input('Combien de Bots ?: '))
    inte=0
    if bot !=0:
        inte= int(input("Niveau D'intelligence des bots? (1 / 2 / 3): "))

        for i in range(bot):
            L.append('bot'+str(i+1))
            print(L[-1],'initialisé !')

    L.append("croupier")
    return L,inte

def Init_scores(joueurs,v=0):
    """
    Renvoie un dictionaire associant chaque joueur a un score v.
    """
    d={}
    for i in joueurs:
        d[i]=v
    return d

def Init_gains(joueurs,s=100):
    """
    Renvoie un dictionaire associant chaque joueur a un montant s.
    """
    d={}
    for i in joueurs:
        if i!='croupier':
            d[i]=s
        else:
            d[i]=0
    return d




def gagnant(score):
    """
    Determine les joueurs qui ne perdent pas le partie (score entre celui du croupier 
    et 21)
    
    Renvoie une liste de ces joueurs.
    """
    cr=score['croupier']
    l=list(score.values())
    l = [v for v in l if v <= 21 and v>=cr]
    
    if len (l)==1:
        return [0]
    else:
        return [x for x in score if score[x] in l and x!='croupier']
        #win=max(l)
        #return [k for k in score if score[k] == win]









