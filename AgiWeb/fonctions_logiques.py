# coding: utf-8
import sqlite3 as lite
import time

def transformation(a):#on transforme la chaine pour qu'elle soit traitable
	c=a
	supprimable = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â',' ', '-', '_','.', ',',"'",'!' ,':', '/']
	correct = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', '', '', '', '', '','', '', '', '']
	for i in range(len(supprimable)):
		c=c.replace(supprimable[i],correct[i])
	c=c.lower()
	return(c)
	
def compare_nom(a,b):#On regarde si a est dans b, b est une liste
	A=transformation(a)
	B=[]
	for i in range(len(b)):
		B.append(transformation(b[i])) 
	if A in B:
		return(True)
	return(False)

def liste(b):#transforme un dictionnaire en liste
	c=[]
	for chaque in b:
		c.append(chaque[0])
	return(c)

def creer_id(b):#créé un id
	c=liste(b)
	taille=len(c)
	if taille==0:
		ide=1
	else:
		ide=max(c)+1
	return(ide)

def ajouter_piece_dans_kit (x=0):
    if x==0 :
        #on crée un id
        contenu =""
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT id FROM kit;")
        ide = creer_id(liste(cur.fetchall()))
        con.close()
        #On choisit et vérifier le nom du kit
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom FROM piece;")
        base=liste(cur.fetchall())
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_kit' value=''>"
        nom_kit=str(request.args.get('nom_kit',''))
        c=compare_nom(nom_kit,base)
        if c:
			#le nom du kit est déjà existant, on revient au départ
			contenu += "<br/>"
			contenu += "Erreur le nom existe déjà"
			contenu += "<br/>"
			contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
			contenu += "<br/>"
			time.sleep(5)
			return(ajouter_piece_dans_kit())
		else:
			#le nom est bon, on crée le kit dans la base kit
			cur.execute("INSERT INTO kit('id_kit', 'nom_kit') VALUES (?,?)", (ide,nom))
			return(ajouter_piece_dans_kit(ide))
    #Maintenant que le kit est créé on va le modifier
    else:
        contenu += "<br/>"
        contenu += "Entrer le nom puis la quantite de pièce"
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_piece' value=''>"
        contenu += "<input type='str' name='quantite' value=''>"
        contenu += "<input type='submit' value='Valider'>"
        nom_piece=str(request.args.get('nom_piece',''))
        quantite=request.args.get('quantite','')
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom FROM piece")
        ligne=liste(cur.fetchall())
        c=compare_nom(nom_piece,ligne)
        if c :
			#le nom est existe
			try:
				quantite=int(quantite)
				quantite>0
			except:	
				#la quantite n'est pas bonne
				contenu += "<br/>"
				contenu += "Erreur la quantite est n'est pas bonne"
				contenu += "<br/>"
				contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
				contenu += "<br/>"
				time.sleep(5)
				return(ajouter_piece_dans_kit(x))
			else:
				#la quantité est un entier positif
				con = lite.connect(cheminbdd)
				con.row_factory = lite.Row
				cur=con.cursor()
				cur.execute("INSERT INTO compo_kit('kit', 'piece','quantite') VALUES (?,?,?)", (x,nom_piece,quantite))#On insert la nouvelle piece dans le kit
		else:
			#le nom de la pièce n'est pas bon
			contenu += "<br/>"
			contenu += "Erreur la pièce n'existe pas"
			contenu += "<br/>"
			contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
			contenu += "<br/>"
			time.sleep(5)
			return(ajouter_piece_dans_kit(x))
		#On affiche la composition du kit
		con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT kit, piece, quantite FROM compo_kit")
        lignes=cur.fetchall()
        con.close()
        contenu += render_template('affichage_personnes.html', personnes = lignes)
