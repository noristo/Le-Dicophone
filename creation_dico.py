# -*- coding: utf-8 -*-

import json


with open('./Ressources/lang/dico_frwiktionary-20200301_v2.json',encoding="utf-8") as f: #création du dico phon sous forme phon[phonème]=[mot1,mot2,mot3] les mots choisis auront la même écriture API
  data = json.load(f)

tmp = {} #dictionnaire final

for keyd,valued in data.items():#pour chaque clé du dictionnaire on supprime les espaces/liaison/marqeur de séparation pour l'enregistrer comme valeur du dictionnaire tmp
	for i in range (0,len(valued)):
		valued[i]=valued[i].replace('.','')
		valued[i]=valued[i].replace(' ','')
		valued[i]=valued[i].replace('‿','')
		if valued[i] in tmp:#si le mot  phonétisé existe dans tmp on ajoute le mot associé à la même clé
			tmp[valued[i]].append(keyd)
		else: # on crée une nouvelle entrée
			tmp[valued[i]] = [keyd]
   
#-----------------------------------------------
handle=open("./Ressources/lang/dico.csv","r",encoding="utf8") 
dicoDef={}
for ligne in handle.readlines(): # pour chaque ligne du fichier dico.csv on prend le mot+numéro de déf+cat gramm+définition
	listefinale=[]
	listeligne=ligne.split("\t",12)
	entre=listeligne[0] #le mot
	#on transforme les mots contenant ' en  ’
	if "'" in entre:
		entre=entre.replace("'","’")
	#on cible les verbe pronominaux
	voy=["a",'i',"é","è","e","ê","o","u"] 
	if listeligne[2]=="(s)": #(s) est écrit dans dico.csv pour marquer les verbes pronominaux
		if entre[0] in voy: #si le mot commence par une voyelle on ajoute s'
			entre="s’"+entre
		else:
			if entre[:2]!="ne" : #cible les expression qui commencent par ne et contiennent deja "se"
				entre="se "+entre
		# ~ print(entre)
		# ~ listefinale.append(entre)
	listefinale.append(entre);listefinale.append(listeligne[1]);listefinale.append(listeligne[6]);listefinale.append(listeligne[9])#entre->mot ;1->numéro de définition;6->catégorie gramm; 9-> définition du mot  
	if listefinale[1]!="" and listefinale[1]!="1":  #si la clé dicoDef[mot] existe dejà
		try:
			dicoDef[listefinale[0]].append(listefinale[1:]) #on rajoute numéro de déf+cat gramm+définition
		except: 
			pass
	else:	 
		dicoDef[listefinale[0]]=[listefinale[1:]] #sinon on crée une nouvelle entrée 

#----------------------------------------------------
with open("./Ressources/L1/ar.txt","r",encoding="utf8") as ar,open("./Ressources/L1/fr.txt","r",encoding="utf8") as fr,open("./Ressources/L1/es.txt","r",encoding="utf8") as es: # ouvre les ressources langagière de chaque langue L
	listeressources=[ar,fr,es]
	nomressources=["ar","fr","es"]
	dicoL1={}
	for i in range(0,len(listeressources)): #pour chaque fichier de langue
		liste=[]
		for ligne in listeressources[i].readlines(): #pour chaque ligne on prend le premier élément comme phonème correct et le deuxième comme faute fréquente
			try:
				listeligne=ligne.split("->",2)
				phoncorr=listeligne[0]
				phonerr=listeligne[1]
				liste.append((phonerr[:-1],phoncorr))
			except:
				pass
		nom=nomressources[i]		
		dicoL1[nom]=liste # on crée un dictionnaire avec la L1 comme clé et les tuples (faute,correction) comme valeur
	# ~ print(dicoL1)
#----------------------------------------------------
with open('./Ressources/lang/dict.json', 'w',encoding="utf-8") as save, open('./Ressources/lang/phon.json', 'w',encoding="utf-8") as fp,open("./Ressources/L1/L1.json", 'w',encoding="utf-8") as L1: #on enregistre les dictionnaires sous format .json
    json.dump(dicoDef, save, ensure_ascii=False)
    json.dump(tmp, fp, ensure_ascii=False)
    json.dump(dicoL1, L1, ensure_ascii=False)
