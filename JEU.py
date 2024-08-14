from initialisations import *
from IA import *
import time
import pygame as pg


#associe chaque cartes au png correspondant
global dico_cartes
dico_cartes= {'As de Carreau': 'as_carreau.png', '2 de Carreau': '2_carreau.png', '3 de Carreau': '3_carreau.png', '4 de Carreau': '4_carreau.png', '5 de Carreau': '5_carreau.png', '6 de Carreau': '6_carreau.png', '7 de Carreau': '7_carreau.png', '8 de Carreau': '8_carreau.png', '9 de Carreau': '9_carreau.png', '10 de Carreau': '10_carreau.png', 'Vallet de Carreau': 'v_carreau.png', 'Dame de Carreau': 'd_carreau.png', 'Roi de Carreau': 'r_carreau.png', 'As de Coeur': 'as_coeur.png', '2 de Coeur': '2_coeur.png', '3 de Coeur': '3_coeur.png', '4 de Coeur': '4_coeur.png', '5 de Coeur': '5_coeur.png', '6 de Coeur': '6_coeur.png', '7 de Coeur': '7_coeur.png', '8 de Coeur': '8_coeur.png', '9 de Coeur': '9_coeur.png', '10 de Coeur': '10_coeur.png', 'Vallet de Coeur': 'v_coeur.png', 'Dame de Coeur': 'd_coeur.png', 'Roi de Coeur': 'r_coeur.png', 'As de Pic': 'as_pic.png', '2 de Pic': '2_pic.png', '3 de Pic': '3_pic.png', '4 de Pic': '4_pic.png', '5 de Pic': '5_pic.png', '6 de Pic': '6_pic.png', '7 de Pic': '7_pic.png', '8 de Pic': '8_pic.png', '9 de Pic': '9_pic.png', '10 de Pic': '10_pic.png', 'Vallet de Pic': 'v_pic.png', 'Dame de Pic': 'd_pic.png', 'Roi de Pic': 'r_pic.png', 'As de Trefle': 'as_trefle.png', '2 de Trefle': '2_trefle.png', '3 de Trefle': '3_trefle.png', '4 de Trefle': '4_trefle.png', '5 de Trefle': '5_trefle.png', '6 de Trefle': '6_trefle.png', '7 de Trefle': '7_trefle.png', '8 de Trefle': '8_trefle.png', '9 de Trefle': '9_trefle.png', '10 de Trefle': '10_trefle.png', 'Vallet de Trefle': 'v_trefle.png', 'Dame de Trefle': 'd_trefle.png', 'Roi de Trefle': 'r_trefle.png'}



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
            
            #Maj ecran: carte tirée par le croupier et son score:
			fen.blit(pg.image.load('cartes/'+str(dico_cartes[s])),(pos_carte['croupier'][0],pos_carte['croupier'][1]))
			fen.blit(pg.image.load('images/'+str(score[i])+'.png'),(750,85))
			
			#toute les lignes de ce type dans le programme servent
			#a decaler les cartes pour qu'on voit les precedentes:
			pos_carte['croupier'][0]-=30
			pos_carte['croupier'][1]+=20
			
			#celles-ci, simplement a actualiser l'ecran entier:
			pg.display.flip()
		
		else:                
			
			s = Pioche(paquet,2)
			
			for carte in s:
				if 'As' in carte:
					#on affiche le choix de l'As seulement pour les vrais joueurs:
					if 'bot' in i:
						score[i]+=ValeurCarte(carte,i,score)
					else:
						score[i]+=valeur_as(i)

				else:
					score[i] += ValeurCarte(carte,i,score)
					
				
				#Maj ecran:  on affiche la carte tiree et le nouveau score:
				fen.blit(pg.image.load('cartes/'+str(dico_cartes[carte])),(pos_carte[i][0],pos_carte[i][1]))
				fen.blit(pg.image.load('images/'+str(score[i])+'.png'),(pos_joueurs(joueurs)[i][0],pos_joueurs(joueurs)[i][1]+220))
				pos_carte[i][0]+=30
				pos_carte[i][1]-=20
				pg.display.flip()
				time.sleep(1)
					         
		
		if score[i]==21:
			blackjack(i)

    
    #on enleve de la liste les joueurs qui on deja 21 au premier tour:
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

	#petit cercle (temoin) qui s'allume en vert a cote d'un joueur quand c'est son tour:
	pg.draw.circle(fen, pg.Color('green'), (pos_joueurs(backup)[j][0]-15,pos_joueurs(backup)[j][1]+200),5)
	pg.display.flip()
	
	#test piocher/arreter :
	x=None
	if 'bot' in j:
		print(j,"réfléchi...")
		time.sleep(2)
		x=ContinuerBot(j,dico_scores,pioche,intelligence)	
	
	else:
		x=continuer(j)
	

	#si x=True, le joueur souhaite piocher :
	if x==True:
		#pioche et calcul du nouveau score:
		carte=Pioche(pioche)[0]
		val=0
		if 'As' in carte:
			if 'bot' in j:
				val=ValeurCarte(carte,j,dico_scores)
			else:
				val=valeur_as(j)
			dico_scores[j]+= val
		else:
			val=ValeurCarte(carte,j,dico_scores)
		
			dico_scores[j]+=val


		#MaJ ecran: afficher la carte tiree:
		fen.blit(pg.image.load('cartes/'+str(dico_cartes[carte])),(pos_carte[j][0],pos_carte[j][1]))
		pg.display.flip()
		pos_carte[j][0]+=30
		pos_carte[j][1]-=20
		time.sleep(1)


		#test de défaite et MaJ du temoin en ROUGE si le joueur a perdu:
		if dico_scores[j] > 21:
			fen.blit(pg.image.load('images/perdu2.png'),(pos_joueurs(backup)[j][0]-5,pos_joueurs(backup)[j][1]+215))
			pg.draw.circle(fen, pg.Color('red'), (pos_joueurs(backup)[j][0]-15,pos_joueurs(backup)[j][1]+200),5)
			pg.display.flip()

			liste_j.pop(liste_j.index(j))
			
		
		#test de victoire du tour.Maj temoin en JAUNE: il signifie que le joueur n'as plus d'actions
		# a faire pendant cette partie (blackjack ou s'est arreter de piocher) mais il n'as pas perdu:
		elif dico_scores[j]==21:
			fen.blit(pg.image.load('images/21.png'),(pos_joueurs(backup)[j][0],pos_joueurs(backup)[j][1]+220))
			pg.draw.circle(fen, pg.Color('yellow'), (pos_joueurs(backup)[j][0]-15,pos_joueurs(backup)[j][1]+200),5)
			blackjack(j)
			
			liste_j.pop(liste_j.index(j))
		
		else:
			fen.blit(pg.image.load('images/'+str(dico_scores[j])+'.png'),(pos_joueurs(backup)[j][0],pos_joueurs(backup)[j][1]+220))
			pg.draw.circle(fen, pg.Color('grey'), (pos_joueurs(backup)[j][0]-15,pos_joueurs(backup)[j][1]+200),5)
			pg.display.flip()
	

	#si x=False, Maj temoin en JAUNE:
	else:
		pg.draw.circle(fen, pg.Color('yellow'), (pos_joueurs(backup)[j][0]-15,pos_joueurs(backup)[j][1]+200),5)
		liste_j.pop(liste_j.index(j))




def tourCroupier(dico_scores,paquet):
	"""
	Pour le role du croupier, on choisira les regles originales du blackjack.
	Elles ne font pas de lui un joueur comme les autres qui doit avoir des strategies.
	Il suit simplement les regles qui lui sont imposees.(cf raport) 
	
	Cette fonction peux mettre a jour le score du croupier et la pioche.
	Elle ne renvoie rien.
	"""
	#pioche tant qu'il n'as pas atteint 17+ :
	while dico_scores['croupier']<17:	
		carte=Pioche(paquet)[0]
		dico_scores['croupier']+=ValeurCarte(carte,'croupier',dico_scores)		
		
		fen.blit(pg.image.load('cartes/'+str(dico_cartes[carte])),(pos_carte['croupier'][0],pos_carte['croupier'][1]))
		
		#On affiche soit son score final, soit la croix de defaite si son score>21.
		if dico_scores['croupier']<=21:
			fen.blit(pg.image.load('images/'+str(dico_scores['croupier'])+'.png'),(750,85))		
		else:
			fen.blit(pg.image.load('images/perdu2.png'),(745,80))
		
		pg.display.flip()
		
		pos_carte['croupier'][0]-=30
		pos_carte['croupier'][1]+=20
		
		time.sleep(2)
	

	if dico_scores['croupier']==21:
		blackjack('croupier')

		





def tourComplet(liste_j,dico_scores,pioche,tour,inte):
	"""
	Fait jouer un tour a tout les joueurs encore en jeu.
	
	Cette fonction appelle tourJoueur() pour chaque joueur encore en jeu
	Elle ne renvoie rien.
	"""

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
	resultats. 
	
	"""
	####MISES
	mises={}	

	#pour chaque joueurs(hors croupier) on utilise question() pour recupere sa mise, et les fonctions IA pour les bots:
	for i in liste_j:
		if i!='croupier':
			
			if 'bot' in i:
				mises[i]=MiseBot(i,gains[i],inte,pioche)
				print(i,'mise',mises[i],'€.')
				gains[i]-=mises[i]

			else:
				mises[i] = question(442,275,'mise de '+str(i)+' ('+str(gains[i])+'€ restants) :')
				#filtre pour avoir un entier:
				if mises[i].isnumeric()==False:
					while mises[i].isnumeric()==False:
						mises[i] = question(442,275,'Entrez un entier:'+'   ('+str(gains[i])+'€ restants)')
				mises[i]= int(mises[i])
				
				while mises[i]<=0 or mises[i]>gains[i]:
					mises[i] = int(question(442,275,'Un entier entre 1 et '+str(gains[i])))
				
				gains[i]-=mises[i]

			#affiche les jetons et la mise:
			fen.blit(pg.image.load('images/jetons.png'),(pos_joueurs(backup)[i][0]+70,pos_joueurs(backup)[i][1]+220))
			fen.blit(font2.render(str(mises[i]), True, pg.Color('black')), (pos_joueurs(backup)[i][0]+80,pos_joueurs(backup)[i][1]+215))
	
	####
	####premier tour
	dico_scores,liste_j=FirstTour(liste_j,pioche,gains,mises)
	

	####
	####Partie	

	#on trace le temoin GRIS (aucune action en cours) pour chaque joueur:
	for i in liste_j:
		if i!='croupier':
			pg.draw.circle(fen, pg.Color('grey'), (pos_joueurs(backup)[i][0]-15,pos_joueurs(backup)[i][1]+200),5)
	
	
	tour=[2]

	#on effectue des tours complet dant que la partie n'est pas fini
	liste_j=[x for x in liste_j if x != "croupier"]
	while partiefinie(liste_j,dico_scores)==False:
		tourComplet(liste_j,dico_scores,pioche,tour,inte)

	#créér un liste de tout les joueurs qui n'ont pas dépassé 21 afin de tester 
	#l'utilité de faire le tour du croupier (inutile si tout les joueurs on 'sauté'):
	l=[x for x in dico_scores.keys() if x!='croupier' and dico_scores[x]<21] 
	if len(l)!=0:
		tourCroupier(dico_scores,pioche)
	
	#si le croupier depasse 21, on mets son score a zero car tout les jouers entre 0 et 21 gagnent:
	if dico_scores['croupier']>21: 
		dico_scores['croupier']=0

			
	gagnants=gagnant(dico_scores)
		

	####
	####affichage vaiqueur(s) et MaJ des gains
		
	#pour chaque joueurs dans la liste de depart, on test le score final:
	for i in backup:
	
		if i in gagnants and i !='croupier':
				
			# +1.5 xla mise  (paye 3:2)
			if dico_scores[i]==21:
				fen.blit(pg.image.load('images/jetons.png'),(pos_joueurs(backup)[i][0]+130,pos_joueurs(backup)[i][1]+220))
				fen.blit(pg.image.load('images/jetons2.png'),(pos_joueurs(backup)[i][0]+190,pos_joueurs(backup)[i][1]+235))	
				gains[i] += int(mises[i]*2.5)
					
			# +1x la mise    (paye 1:1)
			elif dico_scores[i]> dico_scores['croupier']:
				fen.blit(pg.image.load('images/jetons.png'),(pos_joueurs(backup)[i][0]+130,pos_joueurs(backup)[i][1]+220))
				gains[i] += int(mises[i]*2)

			# recuper simplement la mise
			elif dico_scores[i]==dico_scores['croupier']:		
				gains[i] += int(mises[i])
			
		#les perdants ne récuperent pas leurs mise, on affiche un croix sur leurs jetons:
		else:
			if i!='croupier':
				fen.blit(pg.image.load('images/pertemise.png'),(pos_joueurs(backup)[i][0]+60,pos_joueurs(backup)[i][1]+210))

	
	pg.display.flip()
	time.sleep(4)






####====================================================================================
####Programme principal
####
def Jeu():
	"""
	Initialise les joueurs/bot avec start(), creer les variables necessaire tel que
	les gains, la pioche,... .Lance ensuite des partie tant que des joueurs jouent encore a la table en testant a chaque fois: les faillites, si les joueurs veulent continuer
	
	Renvoie le nombre total de parties
	"""
	parties=0
	
	joueurs,intelligence=start(),3
	
	#possibilité de remplir les emplacements restant par des bots (niveau 3):
	if len(joueurs)<4:
		rep=question(442,275,'ajouter des Bots?     (oui/non)')
		while rep!='oui' and rep!='non':
			rep=question(442,275,'ajouter des Bots?     (oui/non)??')
		if rep=='oui':
			for i in range(4-len(joueurs)):
				joueurs.append('bot'+str(i))	
	
	joueurs.append('croupier')
	
	#on a besoins de ces 2 variables a enormement d'endroits dans le programme:
	global pos_carte
	global backup
	backup=joueurs
		
	
	gains=Init_gains(joueurs)
	play=True
	pioche=InitPioche(6)
	
	#boucle des parties (s'arrete si il n'y a lus de joueur a la table):
	while play==True:
		#on remmet la table a 0 au debut de chaque parties:
		clear_total()		
		
		#afficher le nom des joueurs sur leur emplacements:
		pos_carte=pos_joueurs(joueurs)
		for i in joueurs:
			if i!='croupier':
				fen.blit(font.render(i, True, pg.Color('black')), (pos_joueurs(backup)[i][0]+10,pos_joueurs(backup)[i][1]+173))

		# recharge de la pioche si il n'ya plus assez de cartes
		if len(pioche)<100: 
			pioche=InitPioche(6)
		
		joueurs=backup		
		partie(joueurs,pioche,gains,intelligence)
	

		#test de faillite des joueurs:
		for i in [x for x in joueurs if x != "croupier"]:
			if gains[i]==0:
				backup.pop(backup.index(i))
				del gains[i]
				print(i,'est ruiné...')

	
		
		#proposition d'arreter de jouer. Les bots s'arretent au bout de 10 parties max (changeable)
		# et les joueurs quand ils veulent:
		for i in [x for x in joueurs if x != "croupier"]:
			if 'bot' in i:
				if parties>=10:
					backup.pop(backup.index(i))
					print(i,"s'en va avec",gains[i],'€.')
					resultat=gains[i]
					del gains[i]

			elif question(442,275,str(i)+', rejouer ? (reste '+str(gains[i])+'€)')=='non':
				backup.pop(backup.index(i))

								
		

		# play devient False si il n'y a plus de joueurs a la table
		if len([x for x in joueurs if x != "croupier"])==0:			
			play = False
		print(gains)
		parties+=1
	
	print('nombre de parties: ',parties)

	return parties



####==============================================================================
####Fonctions pour l'interface
####

def clear_requete():
	"""
	Remets l'ecran dans l'etat precedent la derniere requete pour l'effacer(afin d'eviter de 
	retracer chaque element dans l'ordre).
	Pour ce faire, on prends soin de sauvegarder l'ecran (sans compression au format png) 
	avant chaque affichage de requettes (questions, boutons...).

	Cette fonction affiche simplement cette capture d'ecran.
	"""
	pg.init()
	fond= pg.image.load("screenshot.png")
	fond = pg.transform.scale(fond, (1285, 750))
	fen.blit(fond,(0,0))
	pg.display.flip()

def clear_total():
	"""
	Remets l'ecran de debut de partie (seulemnt la table et le paquet de cartes retournees).
	"""
	pg.init()
	fond= pg.image.load("images/fond2.png")
	fond = pg.transform.scale(fond, (1285, 750))
	fen.blit(fond,(0,0))
	pg.display.flip()

def question(x,y,texte):
	"""
	Permet de creer une fenetre avec un question et une zone de saisie afin d'en retourner
	la reponse.
	"""
	pygame.image.save( fen, 'screenshot.png' ) #on capture l'ecran avant d'afficher la requete

	fen.blit(pg.image.load('images/questions2.png'),(x,y))
	fen.blit(font.render(texte[:20], True, pg.Color('black')), (x+45, y+8))
	fen.blit(font.render(texte[20:], True, pg.Color('black')), (x+45, y+45))
	
	input_box = pg.Rect(x+24, y+110, 352, 67)	
	text = ''
	fin = False

	#tant que RETURN n'as pas ete presse, on ajoute a la variable texte chaque touche
	# appuyee par l'utilisateur et on l'affiche en meme temps.
	while not fin:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				fin = True			
			if event.type == pg.KEYDOWN:
				if True:
					if event.key == pg.K_RETURN:

						fin=True
					elif event.key == pg.K_BACKSPACE:
						text = text[:-1]
					else:
						text += event.unicode
		
		
		#on remets la fenetre de question vide dans le cas ou un caractere a ete efface:
		fen.blit(pg.image.load('images/questions2.png'),(x,y))
		fen.blit(font.render(texte[:20], True, pg.Color('black')), (x+45, y+8))
		fen.blit(font.render(texte[20:], True, pg.Color('black')), (x+45, y+45))
		#puis on ajoute le texte actuel:
		txt_surface = font.render(text, True, pg.Color('black'))
		fen.blit(txt_surface, (input_box.x+60, input_box.y+5))
		
		pg.display.flip()
	

	clear_requete()  #ecran rétabli 
	return text



def start():
	"""
	initialise la liste des joueurs avec plusieurs appels de question()
	"""
	
	#demander nombre de joueurs:
	nbr=question(442,275,"nombre de joueurs?      (entre 0 et 4)")
	while not nbr.isnumeric():
		nbr=question(442,275,"Erreur. Veuillez    entrer un entier")

	#demander le nom des joueurs:
	liste_j=[]
	for i in range(int(nbr)):		
		liste_j.append(question(442,275,'prenom du joueur '+str(i+1)+' :'))
	
	return liste_j



def pos_joueurs(joueurs):
	"""
	renvoie un dictionnaire des positions des cartes de chaque joueur en fonction du nombre de joueurs
	(4 joueurs max pour eviter un affichage trop dense est illisible)
	"""
	if 'croupier' in joueurs:
		x=len(joueurs)-1
	else:
		x=len(joueurs)
	d={}
	if x==1:
		d[joueurs[0]]=[580,470]

	elif x==2:
		d[joueurs[0]]=[258,470]
		d[joueurs[1]]=[901,470]

	elif x==3:
		d[joueurs[0]]=[258,470]
		d[joueurs[1]]=[580,470]
		d[joueurs[2]]=[901,470]


	elif x==4:
		d[joueurs[0]]=[195,470]
		d[joueurs[1]]=[450,470]
		d[joueurs[2]]=[708,470]
		d[joueurs[3]]=[965,470]

	d['croupier']=[580,15]

	return d




def valeur_as(j):
	"""
	Demande a l'utilisateur la valeur desiree d'un As avec 2 boutons (1 ou 11)
	"""
	pygame.image.save(fen, 'screenshot.png')

	#affichage des boutons/ phrase question:
	fen.blit(pg.image.load('images/as1.png'),(561,325))
	fen.blit(pg.image.load('images/as11.png'),(683,325))
	fen.blit(pg.image.load('images/txt_bleu.png'),(490,200))
	fen.blit(font.render(str(j)+' :', True, pg.Color('black')), (580,210))	
	fen.blit(font.render("Valeur de l'As ?",True,pg.Color('black')),(520,250)) 
	pg.display.flip()

	
	fin = False
	res=0
	while not fin:
		for event in pg.event.get():		
			if event.type == pg.MOUSEBUTTONDOWN:
				#teste de collisions entre la souris et le boutton (position souris dans bouton?)
				if pg.Rect(561,325,80,80).collidepoint(event.pos):
					res=1
					fin=True

				elif pg.Rect(683,325,80,80).collidepoint(event.pos):
					res=11
					fin=True
			
	clear_requete()

	return res



def blackjack(j):
	"""
	affiche le logo d'un blackjack pendant 3 secondes
	"""
	pygame.image.save( fen, 'screenshot.png' )
			
	fen.blit(pg.image.load('images/blackjack.png'),(442,175))
	pg.display.flip()
			
	time.sleep(3)
	clear_requete()
	

def continuer(j):
	"""
	Fonction qui demande a un joueur j si il souhaite jouer une nouvelle partie
	
	Elle renvoie un Booleen.
	"""
	pygame.image.save(fen, 'screenshot.png')

	#affichage des boutons/ phrase question:
	fen.blit(pg.image.load('images/tirer.png'),(1058,80))
	fen.blit(pg.image.load('images/arreter.png'),(258,80))
	fen.blit(pg.image.load('images/txt_orange.png'),(480,220))
	fen.blit(font.render(str(j)+' :', True, pg.Color('black')), (585,230))
	fen.blit(font.render("Tirer ou arreter ?",True,pg.Color('black')),(510,270)) 
	pg.display.flip()
	

	fin = False
	reponse=0
	while not fin:
		for event in pg.event.get():		
			if event.type == pg.MOUSEBUTTONDOWN:
				#test collision bouton TIRER:
				if pg.Rect(1058,80,150,1500).collidepoint(event.pos):
					reponse=True
					fin=True  
				#test collision bouton ARRETER:
				elif pg.Rect(258,80,150,150).collidepoint(event.pos):
					reponse=False
					fin=True
	
	clear_requete()
	return reponse




######
###### LANCEMENT PROGRAMME:
#py jeu.py


#on initialise la table et la police d'ecriture Pygame
fen = pg.display.set_mode((1285,750))
pg.init()
fond= pg.image.load("images/fond2.png")
fen.blit(fond,(0,0))


font = pg.font.SysFont('comicsansms', 35)
font2 = pg.font.SysFont('comicsansms', 20)

pg.display.flip()




#c'est parti !
Jeu()

