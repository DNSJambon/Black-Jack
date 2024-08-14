from random import *
from initialisations import *
import math


def ContinuerBot(j,dico_scores,pioche,intelligence):
	"""
	Renvoie le choix de continuer d'un bot (booleen) avec une intelligence de 1 a 3
	en appelant la bonne fonction.

	Renvoie un Booleen
	"""
	if intelligence==1:
		r=choixIdiot()
		if r==False:
			print(j,'Ne continue pas')
		return r

	elif intelligence ==2:
		r=choixAmateur(dico_scores[j])
		if r==False:
			print(j,'Ne continue pas')
		return r
	else:
		r=choixExpert(dico_scores[j],pioche)
		if r==False:
			print(j,'Ne continue pas')
		return r



def MiseBot(j,gains,intelligence,pioche):
	"""
	Renvoie la mise d'un bot (booleen) avec une intelligence de 1 a 3
	en appelant la bonne fonction.

	Renvoie un entier
	"""
	if intelligence==1:
		return miseIdiot(gains)
	elif intelligence==2:
		return miseAmateur(gains)
	else:
		return miseExpert(gains,pioche)






#niveau d'intelligence (1)(aleatoire total)
def choixIdiot():
	"""
	Renvoie un booleen avec 50% de chance pour chacun.
	"""
	return choice([True,False])

def miseIdiot(gains):
	"""
	Renvoie un entier aleatoire entre 1 et l'agrent disponible
	"""
	return randint(1,gains)




#niveau d'intelligence (2)
"""
il va decider de continuer ou non en prennant uniquement compte de son score (+ ou - proche de 21),
comme un joueur amateur (intuitif)
"""
def choixAmateur(score):
	"""
	Renvoie un booleen choisi avec des probabilites intuitives selon le score
	"""
	ecart = 21 - score
	#on associe l'ecart a la chance que le joueur a de NE PAS perdre en continuant (on considere
	#seulement les 13 valeurs possible a chances egales sans savoir si elles sont encore
	#presenete dans la pioche et en quelles quantite).
	#Exemple: pour 18 (ecart a 21 = 3) il y a 3 cartes qui ne sont pas eliminatoires (AS, 2 et 3)
	#donc 3 chances sur 13 (~23.1%) de continuer a jouer.
	proba={1:7.7, 2:15.4, 3:23.1, 4:30.8, 5:38.5, 6:46.2, 7:53.8, 8:61.5, 9:69.1}

	#la valeur ne peux pas etre >10 donc si ecart>10 on continue forcement (proba 100%):
	for i in range(10,20):
		proba[i]=100

	return choices([True,False], weights=(proba[ecart],100-proba[ecart]), k=1)[0]

def miseAmateur(gains):
	"""
	Renvoie la moitié des gains
	"""
	return gains//2+1




#niveau d'intelligence (3) (QI = 300+)
"""
Simule un excellent joueur capable de connaitre les chances qu'il a de réussir
en fonction des cartes restantes dans le paquet (qu'il connait en memorisant chaque
carte tiree).
"""
def choixExpert(score,pioche):
	"""
	Renvoie un booleen en prenant compte des carte encore presentent dans le paquet
	et en calculant la chance qu'on a de ne pas depasse 21.
	"""
	ecart = 21 - score
	chance=0
	for i in pioche:
		if ValeurCarte(i,'bot',{'bot':11}) <= ecart:
			chance+=1


	return choices([True,False], weights=(chance/len(pioche)*100,100-(chance/len(pioche)*100)), k=1)[0]


"""
On va utiliser la methode de comptage de cartes Hi-Lo.
"""
def miseExpert(gains,pioche):
	"""
	Renvoie une mise calculee en fonction du score qu'on obtient en utilisant la methode
	Hi-Lo qui associe chaque carte tiree a un score.
	Exemple: si le score Hi-Lo du paquet est -3, alors le score des carte tiré est 3, car 		le score du paquet total est toujours de 0.
	"""
	Rc={1:-1,2:1,3:1,4:1,5:1,6:1,7:0,8:0,9:0,10:-1}
	RC=0
	for i in pioche:
		RC+= Rc[ValeurCarte(i,'bot',{'bot':11})]
	RC = -RC

	restant= round(len(pioche)/52)
	Tc= RC/restant

	if Tc>=4:
		return math.ceil(gains/100*90)
	elif Tc>2 and Tc<4:
		return math.ceil(gains//2+(gains/100*Tc*10))
	elif Tc>0 :
		return math.ceil(gains/100*60)
	elif Tc==0:
		return math.ceil(gains/2)
	elif Tc>0 and Tc>-4:
		return math.ceil(gains//2-(gains/100*abs(RC)*10))
	else:
		return math.ceil(gains/100*10)




