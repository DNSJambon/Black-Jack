from initialisations import *
from IA import *
import sys, os
import time
import pygame



def continuer(j):
	"""
	Fonction qui demande a un joueur j si il souhaite jouer une nouvelle partie
	
	Elle renvoie un Booleen.
	"""
	rep= input(str(j)+", voulez vous continuer? (oui/non): ")
	while rep!='oui' and rep!='non':
		rep= input(str(j)+", voulez vous continuer? (oui/non): ")

	if rep=='oui':
		return True
	else:
		return False

def FirstTour(joueurs,paquet,gains,mises):
    """
    Joue le premier tour du BlackJack en piochant 2 cartes pasr joueurs et une seule
    pour le croupier.
    
    Met a jour et renvoie le dico des scores et la liste des joueurs.
    """
    print("\n========================= Premier Tour ==========================")
    score=Init_scores(joueurs)
    for i in joueurs:
        if i=='croupier':
            s=Pioche(paquet,1)[0]
            score[i]= ValeurCarte(s,i,score)
            print("\nLe croupier a tiré:",s,". Son score est donc",score[i])
        
        else:
            print(i,'reçoit ses cartes')
            
            
            s = Pioche(paquet,2)
            score[i] = ValeurCarte(s[0],i,score)
            score[i] +=ValeurCarte(s[1],i,score)
            print(i,"a tiré:",s[0],"et",s[1],". Son score est donc",score[i],'\n')
            

        if score[i]==21:
            print(i,' a fait un BlackJack!\n')
        time.sleep(4)
    
    x=[]
    for i in range(len(joueurs)):
        if score[joueurs[i]]!=21:
            x.append(joueurs[i])
    joueurs=x.copy()


    return score,joueurs

def tourJoueur(j,dico_scores,pioche,tour,liste_j,intelligence):
	"""
	contrairement au BlackJack ordinaire le tour des joueurs se jouera a tour de roles:
	Les joueurs tirerons des cartes chacun leurs tour et non d'un seul coup jusqu'a 		    s'arreter.
	Cela augmente un peu le suspens...
	
	cette fonction peut mettre a jour la liste des joueurs, le dico des scores et la 
	pioche.
	Elle de renvoie rien
	"""
	print('\n|| Le score de ',j,' est: ',dico_scores[j],', A lui de jouer: ||')
	x=None
	if 'bot' in j:
		print(j,"réfléchi...")
		time.sleep(2)
		x=ContinuerBot(j,dico_scores,pioche,intelligence)	
	
	else:
		x=continuer(j)
	

	if x==True:
		#pioche et calcul du nouveau score:
		carte=Pioche(pioche)[0]
		dico_scores[j]+=ValeurCarte(carte,j,dico_scores)
		print(j,' a tiré:',carte,'| Son score est désormais:',dico_scores[j])
		time.sleep(3)


		#test de défaite:
		if dico_scores[j] > 21:
			print(j,'est éliminé...')
			liste_j.pop(liste_j.index(j))
			
		
		#test de victoire du tour:
		elif dico_scores[j]==21:
			print(str(j)+' a fait un BlackJack!')
			liste_j.pop(liste_j.index(j))
			

	else:
		liste_j.pop(liste_j.index(j))


def tourCroupier(dico_scores,paquet):
	"""
	Pour le role du croupier, on choisira les regles originales du blackjack.
	Elles ne font pas de lui un joueur comme les autres qui doit avoir des strategies.
	Il suit simplement les regles qui lui sont imposees.(cf raport) 
	
	Cette fonction peux mettre a jour le score du croupier et la pioche.
	Elle ne renvoie rien.
	"""
	print("\n======================= Tour du Croupier ===========================")
	while dico_scores['croupier']<17:
		print("Le croupier pioche une carte...")
		time.sleep(2)
		carte=Pioche(paquet)[0]
		dico_scores['croupier']+=ValeurCarte(carte,'croupier',dico_scores)
		
		print('Le croupier a tiré:',carte,'| Son score est désormais:',dico_scores['croupier'],'\n')
		time.sleep(3)
		
	if dico_scores['croupier']==21:
		print('Le croupier a fait un BlackJack!')
		




def tourComplet(liste_j,dico_scores,pioche,tour,inte):
	"""
	Fait jouer un tour a tout les joueurs encore en jeu.
	
	Cette fonction appelle tourJoueur() pour chaque joueur encore en jeu
	Elle ne renvoie rien.
	"""
	print("\n========================== Tour n°",tour[0]," ============================")
	l=liste_j.copy()
	for i in range(len(l)):
		tourJoueur(l[i],dico_scores,pioche,tour,liste_j,inte)
	tour[0]+=1



def partiefinie(joueurs,dico_scores):
	"""
	La partie est finie seulement si plus aucun joueur n'est dans le jeu.
	"""
	if len(joueurs)==0:
		return True
	else:
		return False



def partie(liste_j,pioche,gains,inte):
	"""
	Cette Fonction permet de jouer un partie complete des mises jusqu'a l'affichage des
	resultats. Puis
	
	"""
	#MISES
	print("\n=========================== MISES ===============================")
	mises={}	
	for i in liste_j:
		if i!='croupier':
			
			if 'bot' in i:
				mises[i]=MiseBot(i,gains[i],inte,pioche)
				print(i,'mise',mises[i],'€.')
				time.sleep(2)
				gains[i]-=mises[i]

			else:
				mises[i]=int(input(str(i)+", il vous reste "+str(gains[i])+ "€, merci d'indiquer le montant de votre mise: "))
				
				while mises[i]<=0 or mises[i]>gains[i]:
					mises[i]=int(input(str(i)+", il vous reste "+str(gains[i])+ "€, merci d'indiquer le montant de votre mise: "))
				gains[i]-=mises[i]
	print(gains)

	
	#premier tour
	dico_scores,liste_j=FirstTour(liste_j,pioche,gains,mises)
	

	
	#Partie
	tour=[2]
	liste_j=[x for x in liste_j if x != "croupier"]
	while partiefinie(liste_j,dico_scores)==False:
		tourComplet(liste_j,dico_scores,pioche,tour,inte)


	l=[x for x in dico_scores.keys() if x!='croupier' and dico_scores[x]<=21] #créér un liste de tout les joueurs qui n'ont pas dépassé 21 afin de tester l'utilité de faire le tour du croupier(inutile si tout les joueurs on 'sauté').
	if len(l)!=0:
		tourCroupier(dico_scores,pioche)
	
	if dico_scores['croupier']>21: 
		print('Le croupier a perdu, les joueurs encore en jeu gagnent.')
		dico_scores['croupier']=0

			
	gagnants=gagnant(dico_scores)
		
	
	#affichage vaiqueur(s) et MaJ des gains
	print("\n========================== RESULTATS ==============================")
	if 0 not in gagnants:			
			for i in gagnants:
		
				if dico_scores[i]==21:
					print("\n==>",i,"a fait un BlackJack et gagne 1.5x sa mise initiale")			
					gains[i] += int(mises[i]*2.5)
				
				elif dico_scores[i]> dico_scores['croupier']:
					print("\n==>",i,"bat le croupier et gagne 1x sa mise initiale")		
					gains[i] += int(mises[i]*2)

				elif dico_scores[i]==dico_scores['croupier']:
					print("\n==>",i,"a fait égalité avec le croupier et récupere simplement sa mise")			
					gains[i] += int(mises[i])

			for i in dico_scores.keys():
				if i not in gagnants and i!='croupier':
					gains['croupier']+=int(mises[i])


	else:

		print("\nLe croupier bat tout les joueurs restant et remporte toutes les mises...")
		gains['croupier']+= sum(list(mises.values()))	
	
	time.sleep(6)










####====================================================================================
####Programme principal
def Jeu():
	"""
	Initialise les joueurs/bot avec Initjoueurs(), creer les variables necessaire tel que
	les gains, la pioche,... .Lance ensuite des partie tant que des joueurs jouent encore a 	la table en testant a chaque fois: les faillites, si les joueurs veulent continuer
	
	Renvoie le nombre total de parties
	"""
	parties=0

	
	joueurs,intelligence=InitJoueurs(int(input("Combien de joueurs ?: ")))

	backup=joueurs
	gains=Init_gains(joueurs)
	play=True
	pioche=InitPioche(6)
	
	while play==True:
		if len(pioche)<100: 
			pioche=InitPioche(6)
		
		joueurs=backup		
		partie(joueurs,pioche,gains,intelligence)
		print('\n$argent$ des joueurs: ',gains,'\n')
		
		

		#test de faillite:
		for i in [x for x in joueurs if x != "croupier"]:
			if gains[i]==0:
				backup.pop(backup.index(i))
				del gains[i]
				print(i,'est ruiné...')


		
		
		#proposition d'arreter de jouer:
		for i in [x for x in joueurs if x != "croupier"]:
			if 'bot' in i:

				if parties>=5:
					backup.pop(backup.index(i))
					print(i,"s'en va avec",gains[i],'€.')
					resultat=gains[i]
					del gains[i]



			elif input(str(i)+", souhaitez vous rejouer? (oui/non): ")=='non':
				backup.pop(backup.index(i))
				print(i,"s'en va avec",gains[i],'€.')
								
				

		if len([x for x in joueurs if x != "croupier"])==0:
			print('Plus aucun joueur a la table.')
			play = False

		parties+=1
	print('nombre de parties: ',parties)

	return parties



#py jeu.py

Jeu()




