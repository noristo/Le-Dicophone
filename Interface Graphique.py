from tkinter import * 
from tkinter import font as tkFont 
from winsound import *
from fonctions import*

#---------------------------------------Fonction de l'interface graphique-----------------------------------------------------------------------------------------------------------------
class imag():
	#fonction qui produit une image clickable et passe la langue choisis quand on clique // entrée: emplacement des images, la langue choisie, collonne et ligne dans l'interface
	def __init__(self,lien,rowa,collumna,lang):
		self.photo = PhotoImage(file=lien) 
		self.photo = self.photo.subsample(2) #rétrécit l'image
		Label=Button(root,image = self.photo,command=lambda:self.onclick(lang))
		Label.grid(row=rowa, column=collumna)
		frame1.append(Label)
	#fonction qui change de frame et sélectionne le profil langagier et charge le clavier API // entrée: la langue choisie
	def onclick(self,lang):
		global profil
		profil=lang
		for label in frame1: label.destroy()
		for frame in frame2: frame.pack()
		keyboard()
#-------------------#Ajoute une entrée et un bouton info-----------------
def addBox(): 
	global ent
	next_column = len(all_entries)
	# Ajout d'un bouton info dans la première rangée
	lab = Button(frame_for_boxes, text="info",font=helv36,command=lambda:informations(next_column))
	lab.grid(row=0, column=next_column,padx=10)
	all_buttons.append(lab)
	#  Ajout de la case de saisie dans la deuxième rangée
	ent = Entry(frame_for_boxes,font=helv36,width=10)
	ent.grid(row=1, column=next_column)
	all_entries.append(ent)	

#---------------#fonction qui supprime les entrées---------------------
def deleteBox(): 
	global all_entries
	global all_buttons
	#Supprime les case de saisie
	last=all_entries[-1]
	all_entries=all_entries[:-1]
	last.destroy()
	#--------------------
	#Supprime les boutons info
	lastb=all_buttons[-1]
	all_buttons=all_buttons[:-1]
	lastb.destroy()
#-----------------#fonction relative à la partie d'informations pour chaque phonème -------------------
def informations(num):  #entrée le numéro de colonne choisie
	
	#sélectionne le texte de la case choisie
	phon_select=all_entries[num].get()
	#crée une nouvelle fenêtre avec le fichier .txt correspondant 
	window = Toplevel(root)
	info_text=Text(window,width=40,height=5)
	info_text.pack(pady=20)
	fichier_phon=open("./Ressources/info_phoneme/"+phon_select+".txt","r",encoding="utf-8")
	lecture=fichier_phon.read()
	info_text.insert(END,lecture)
	#un bouton pour écouter le phonème
	play=lambda: PlaySound("./Ressources/sons_phoneme/"+phon_select+".wav", SND_FILENAME)
	son=Button(window, text='Ecouter le phonème',command=play)
	son.pack(pady=20)
	fichier_phon.close()
#----------------#fonction relative au clavier--------------------
def keyboard(): 
	buttons=["/","a","ɑ","ɑ̃","ã","b","ɔ","ɔ̃","d","e","ə","ɛ","ɛ̃","f","ɡ",".","ɥ","i","j","k","l","m","n","ɲ","ŋ","o","ø","œ","œ̃","p","?","ʁ","s","ʃ","t","u","v","w","y","z","ʒ"]
	varRow=2
	varColumn=0	
	for button in buttons:	
		command=lambda x=button: select(x)
		Button(frame_for_keyboard,text=button,width=5,font=helv36,bg="#000000",fg="#ffffff",activebackground="#ffffff",activeforeground="#000000",relief='raised',pady=10,bd=10,command=command).grid(row=varRow,column=varColumn)
		varColumn+=1
		if varColumn>14 and varRow==2:
			varColumn=0
			varRow+=1
		if varColumn>14 and varRow==3:
			varColumn=0
			varRow+=1
#-------------#fonction qui permet au clavier d'insérer la valeur dans une case----------------------
def select(value): #entrée valeur du clavier
	focus=root.focus_get()
	focus.insert(END,value)
#-------------#fonction qui lance le script de recherche dicophone et qui ouvre la fenêtre pour afficher le Résultat----------------------	
def valider():
	#var text est la variable qui prendra la suite des phonèmes
	text=""
	#trouvfin est la variable qui va contenir le résultat final
	trouvfin=""
	for i in all_entries: #pour chaque case de saisie on concatène le texte à lui même
		text=text+i.get()
	deftrouv=trouv(text,profil) # on lance le script pour trouver la définition selon le profil choisit
	for ligne in deftrouv: #formatage du résultat affiché 
		trouvfin= "\n"+str(ligne)+trouvfin+"\n"
	if not trouvfin:
		trouvfin="Le mot recherché n'est pas trouvé, Veuillez réessayer d'autres phonèmes"
	#crée une nouvelle fenêtre avec le fichier .txt correspendant 
	window = Toplevel(root)
	Label(window, text =trouvfin, font =('Verdana', 10)).pack(padx=20)

#-------------#fonction qui lance le script de suggestion et qui ouvre la fenêtre pour afficher le Résultat----------------------	
def affichsugg():
	text=""
	for i in all_entries:
		text=text+i.get()
	textsugg=str(suggestion(text))
	#crée une nouvelle fenêtre avec le résultat de la suggestion  
	window2 = Toplevel(root)
	Label(window2, text =textsugg, font =('Verdana', 14)).pack()
#----------------------------------------------------------------------------------------------------------




# création de la fenêtre Tkinter
root = Tk() 
root.iconbitmap("./Images/ico.ico")
root.title("DicoPhone")
#----------------Première Frame---------------------	
#tableau contenant les éléments de la permière frame
frame1=[]		 
helv36 = tkFont.Font(family='Helvetica', size=15, weight='bold') # Police
# ~ # Premier titre
Label1=Label(root, text = 'Bienvenue sur Dicophone\nVeuillez sélectionner votre langue maternelle', font =('Verdana', 15))
Label1.grid(row=0, column=1)
frame1.append(Label1)
#instanciation des images
image1=imag(r"./Images/3.png",3,0,"fr")
image2=imag(r"./Images/1.png",3,1,"ar")
image2=imag(r"./Images/2.png",3,2,"es")
#Variable vide pour la langue
profil=""



#---------------Deuxième Frame----------------------
#tableau contenant les ID des boutons et du entrée
all_entries = []
all_buttons = []
#tableau contenant les IDs de la deuxième frame
frame2=[]

Label1=Label(root, text = "Entrez le mot recherché en ajoutant un phonème à la fois\nAjoutez un '?' si vous n'êtes pas sûr qu'un phonème est compris dans le mot recherché\nou mettez '/' pour ajouter un phonème alternatif\nVous pouvez écrire '.' à la place d'un phonème inconnu", font =('Verdana', 14))
frame2.append(Label1)

#bouons pour ajouter/supprimer une entrée ansi que le bouton valider qui permet de rechercher les phonèmes dans le dictionnaire
showButton = Button(root, text='Supprimer le dernier phonème',font=helv36,fg="Red",command=deleteBox)
frame2.append(showButton)

addboxButton = Button(root, text='Ajouter un phonème',font=helv36, command=addBox)
frame2.append(addboxButton)

addboxButton2 = Button(root, text='Suggestions',font=helv36,fg="blue",command=affichsugg)
frame2.append(addboxButton2)

addboxButton1 = Button(root, text='Valider',font=helv36,fg="Green",command=valider)
frame2.append(addboxButton1)
#création des cases de saisie
frame_for_boxes = Frame(root)
frame2.append(frame_for_boxes)
#appel du clavier
frame_for_keyboard = Frame(root)
frame2.append(frame_for_keyboard)


root.mainloop()
#--------------------------Pour lancer le script sans interface graphique, veuillez activer les commentaires-------------------------------------------
# ~ entre=input("Quel est le mot recherché")
# ~ print(trouv(entre,"fr")) #Veuillez préciser le profil ar/fr/es
