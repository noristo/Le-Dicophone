import json
import re


def remplacephon(s,lang,tour=0):#fonction qui permet de remplacer les erreurs les plus fréquentes par langue L1 // entrée un tableau contenant une suite de phonèmes ou plus et la langue L1// sortie un tableau avec toutes les suggestions
	if tour>=3: # trois tour pour limiter les résultats
		return(s)
	else:
		listepair=dicoL1[lang] #pour chaque paire ex ('ɑ̃','a') on remplace le premier élément par le second et on l'ajoute au tableau s
		for i in listepair:
			premier=i[0]
			second=i[1]
			for elem in s:
				if premier in elem:
					matches=re.finditer(premier,elem) #trouve premier dans le String elem
					index=[match.start() for match in matches]
					for i in index:
						x=elem[:i]+second+elem[i+len(premier):]
						if x not in s:
							s.append(x)
		tour+=1
		return(remplacephon(s,lang,tour))
		
			
def trouv(util,lang): #fonction qui recherche une définition par une entrée API // entrée: une suite de phonèmes // le/les mots correspendants avec leurs définitions
	if "̃?" in util:# cas du caractère ̃  suivi du "?" par ex : ã ?
		j=util.find("̃")
		util=util[:j-1]+"(?:"+util[j-1:j+1]+")"+util[j+2:]
	if "." in util: # cas du "."
		k=util.find(".")
		util=util[:k]+".{1,2}"+util[k+1:] # cas des phonèmes comportant le ̃  qui comptent pour deux	
	if "/" in util:# on change la variable before lorsque le caractère ̃  est présent
		i=util.find('/')
		before=1
		if util[i-1]=="̃":
			before=2
		util=util[:i-before]+"["+util[i-before]+"|"+util[i+1]+"]"+util[i+2:]
	phonementre=[]
	for keyP in phon.keys(): # on recherche mot donné dans la liste des clés du dictionnaire Phon
		entrephon=re.findall(r"^"+util+"$",keyP)
		if entrephon:
			phonementre.append(keyP)
	# si la liste phonementre est vide donc pas de phonème trouvé dans le fichier phon.json alors on appelle la fonction remplacephon
	if not phonementre:
		phonementre=remplacephon([util],"fr")	
	listephon=[]
	for j in phonementre: 
		try:
			listephon.append(phon[j])
		except:
			pass
	# ~ print(listephon)
	
	# ~ # Si on ne trouve pas de mots avec le traitement regex on enlève le "?"
	if not listephon:		
		if "?" in util:
			j=util.find("?") #cas du "?"
			util=util[:j]+util[j+1:]
			listresult=remplacephon([util],"fr")
			for result in listresult:
				try:
					listephon.append(phon[result])
				except:
					pass
	#si la liste listephon est vide donc on n'a pas trouvé de résultats même en corrigeant les erreurs les plus fréquentes en français, on passe en argument le profil langagier de l'utilisateur à la fonction remplacephon()
	if not listephon and lang!="fr":
		phonementre=remplacephon([util],lang)
		for j in phonementre:
			try:
				listephon.append(phon[j])
			except:
				pass

	resultat=[]
	for i in listephon:
		for j in i:
			try:
				resultDico=str(dico[j]) #recherche les clés j de la liste des entrées phonologiques trouvée dans le dictionnaire dico
				stringresult=j.capitalize()+":"+resultDico+"\n"
				resultat.append(stringresult)
			except:
				pass 
	return (resultat)
			
def suggestion (util): #fonction qui permet de donner des suggestions à partir du mot donné // entré une suites de phonèmes // tableau des entrées phon qui commencent par cette suite
	suges=[]
	i=0
	for keyP in phon.keys(): 
		entrephon=re.findall(r"^"+util+".{0,4}",keyP)#on recherche dans la liste phon.keys() la suite des phonèmes donnée + 0 à 4 caractères
		if entrephon:
			suges.append(keyP)
			i+=1
		if i>=10: #on limite le script à 10 résultats
			break;			
	return(suges)

with open('./Ressources/lang/phon.json',encoding="utf-8") as handle1, open('./Ressources/lang/dict.json',encoding="utf-8") as handle2,open('./Ressources/L1/L1.json',encoding="utf-8") as handle3:
	  phon = json.load(handle1)
	  dico = json.load(handle2)
	  dicoL1 = json.load(handle3)



