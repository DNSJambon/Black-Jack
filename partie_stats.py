from initialisations import *
from IA import *
import sys, os
"""
Ce fichier sert uniquement a faire sdes satisitiques sur les bots, pour voir
toute les fonctions commentees, consulter jue.py

"""
#py partie.py

def continuer(j):
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
        
    
    x=[]
    for i in range(len(joueurs)):
        if score[joueurs[i]]!=21:
            x.append(joueurs[i])
    joueurs=x.copy()


    return score,joueurs

def tourJoueur(j,dico_scores,pioche,tour,liste_j,intelligence):
	print('\n|| Le score de ',j,' est: ',dico_scores[j],', A lui de jouer: ||')
	x=None
	if 'bot' in j:
		print(j,"réfléchi...")
		x=ContinuerBot(j,dico_scores,pioche,intelligence)	
	
	else:
		x=continuer(j)
	

	if x==True:
		#pioche et calcul du nouveau score:
		carte=Pioche(pioche)[0]
		dico_scores[j]+=ValeurCarte(carte,j,dico_scores)
		print(j,' a tiré:',carte,'| Son score est désormais:',dico_scores[j])


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

	print("\n======================= Tour du Croupier ===========================")
	while dico_scores['croupier']<17:
		print("Le croupier pioche une carte...")
		carte=Pioche(paquet)[0]
		dico_scores['croupier']+=ValeurCarte(carte,'croupier',dico_scores)
		
		print('Le croupier a tiré:',carte,'| Son score est désormais:',dico_scores['croupier'],'\n')
		
	if dico_scores['croupier']==21:
		print('Le croupier a fait un BlackJack!')
		




def tourComplet(liste_j,dico_scores,pioche,tour,inte):

	print("\n========================== Tour n°",tour[0]," ============================")
	l=liste_j.copy()
	for i in range(len(l)):
		tourJoueur(l[i],dico_scores,pioche,tour,liste_j,inte)
	tour[0]+=1



def partiefinie(joueurs,dico_scores):
	if len(joueurs)==0:
		return True
	else:
		return False



def partie(liste_j,pioche,gains,inte):
	#MISES
	print("\n=========================== MISES ===============================")
	mises={}	
	for i in liste_j:
		if i!='croupier':
			
			if 'bot' in i:
				mises[i]=MiseBot(i,gains[i],inte,pioche)
				print(i,'mise',mises[i],'€.')
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
	
	return gagnant(dico_scores)









####====================================================================================
####Programme principal
def Jeu():
	parties=0
	resultat=0
	

	joueurs,intelligence=['bot1','croupier'],1
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
				resultat=gains[i]
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

	return parties,resultat





#STATISTIQUES:

parties=0
argent=0
benef=0
n=0
p=0
it=5000
sys.stdout = open(os.devnull, 'w')

for i in range(it):
	
	part,r=Jeu()
	if r > 100:
		p+=1
		benef+=r
	else:
		n+=1
	
	parties+=part

sys.stdout = sys.__stdout__
print(parties/it)
print(round(p/it*100,2),"%  des cas sont un gain d'argent (>100€ a la fin)")
print(round(n/it*100,2),"%  des cas sont une perte d'argent (<100€ a la fin)")




