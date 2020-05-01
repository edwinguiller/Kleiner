# coding: utf-8
from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
import time
from constantes import *

def transformation(a):#on transforme la chaine pour qu'elle soit traitable
    c=str(a)
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

def demande_interaction(n,contenu):
	for i in range(n):
		contenu += "<form method='post' action='code_kit'>"
		contenu += "<input type='str' name='nom_kit'+str(i)+'' value='' />"
	contenu += "<input type='submit' value='Envoyer'/> </form>"
	return(contenu)
def recupere_interraction(n,contenu):
	L=[]
	for i in range(n):
		nom=str(request.args.get('nom_kit'+str(i),''))
		L.append(nom)
	return(L)

def modifier_kit(nom_kit,pieces,quantites):#La piece est choisit parmit un menu dérouant donc il n'y a pas besoin de vérifier
	return(ajouter_piece(compo_kit, [piece,quantite], [pieces,quantites], [str(),int()]))

def quantite_bonne(quantite):
	try: #on vérifie que la quantité est bonne
			quantite=int(quantite)
	except: #si la quantité est mauvaise alors message d'erreur
		return([quantite,False])
	else:
		quantite=int(quantite)
		if quantite>0:
			return([quantite,True])
		else:
			return([quantite,False])

def choix_kit(nom_du_kit):#nom_du_kit est une liste ["nom du kit",True/false] selon si on veut modifier ou creer le kit
#la fonction execute l'ordre et retourne une liste [nom_du_kit/None,l'id du kit]    
    
    #On recupère les variables utiles
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur=con.cursor()
    cur.execute("SELECT nom_kit from kit;")
    nom_des_kits=liste(cur.fetchall())
    cur.execute("SELECT id from kit;")
    ids_des_kits=cur.fetchall()
    
    #On crée un kit, car nom_du_kit[1]=True
    if nom_du_kit[1]:
		#le nom existe déjà
        if compare_nom(nom_du_kit[0],nom_des_kits):
            cur.execute("SELECT id from kit WHERE nom_kit=?;",[nom_du_kit[0]])
            id_kit=liste(cur.fetchall())[0]
            return([None,id_kit])
        else:
            id_kit=creer_id(ids_des_kits)
            cur.execute("INSERT INTO kit(id,nom_kit) VALUES (?,?);",[id_kit,nom_du_kit[0]])
            con.commit()
            return([nom_du_kit,id_kit])
    #sinon on modifie un kit existant
    else:
       cur.execute("SELECT id from kit WHERE nom_kit=?;",[nom_du_kit[0]])
       id_kit=liste(cur.fetchall())[0]
       return([nom_du_kit,id_kit])
	

def ajouter_bdd(base, colonne, entree, types): # prend en argument  une base (ex: piece), les colonnes que l'on veut modifier (une liste ex: [id, nom...]), les entrées (valeurs) et le type de ces valeurs

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    contenu =''
    #ecriture de la chaine insert
    selection= "INSERT INTO "+ base + " ("
    valu=""
    for i in colonne:
        selection= selection + i + ", "
        valu=valu + "?,"
    selection=selection[:-2]
    valu=valu[:-1]
    selection= selection + ") VALUES (" + valu +")"

    taille=len(entree)
    if (test_rien(entree)==0):
        if test_types(entree,types)==0:
            cur.execute(selection, (entree))
    con.commit()
    con.close()

def delete (base, colonne, entree): #prend en argument une base (ex: piece), une colonne dans cette base (ex: nom) et supprime la ligne quand la valeur de la colonne vaut nomdele

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    suppr="DELETE FROM " + base + " WHERE " +colonne+ "=?"
    if (entree != ""):
        cur.execute (suppr, [entree])
    con.commit()
    con.close()

def testin (base, colonne, entree): # test si l entree (une seule) est deja dans la bdd pour la colonne (une valeur) return 1 si il y'est et 0 si il n'y est pas

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    selection="SELECT " + colonne + " FROM " + base + ";"
    cur.execute(selection)
    recuperer=cur.fetchall()
    test=[]
    for valeur in recuperer:
        test.append(valeur[0])
    if (entree in test):
        retour=1
    elif (entree not in test):
        retour=0
    else:
        return error
    return retour

def test_rien(entree): # test si les entree (tableau) ne sont pas vide, renvois 1 si une valeur est vide et 0 sinon

    taille=len(entree)
    for i in range (0,taille):
        if (entree[i]==""):
            return 1
    return 0

def test_types(entree,types): #test le type des entrées (tableau) et les entrées (tableau) et renvois 0 si tout est bon et 1 si il y'a un problème

    taille=len(entree)
    for i in range (0, taille):
        if (types[i]==str):
            try:
                entree[i]=str(entree[i])
            except:
                print ("str")
                return 1
        elif (types[i]==int):
            try:
                entree[i]=int(entree[i])
            except:
                return 1

    return (0)

def mise_a_jour_bdd (base, colonne, entree, types): # prend en argument  une base (ex: piece), les colonnes que l'on veut modifier (une liste ex: [id, nom...]), les entrées (valeurs) et le type de ces valeurs et met ajour la ligne de la dernière valeur de colonne qui a comme valeur la derniere d'entree

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    contenu =''
    #ecriture de la chaine insert
    selection= "UPDATE "+ base + " SET "
    for i in colonne:
        if (i==colonne[-1]):
            selection=selection[:-2]
            selection= selection + " WHERE " + i + "=?"
        else:
            selection= selection + i + "=?, "

    print (selection)

    if (test_rien(entree)==0):
        if test_types(entree,types)==0:
            cur.execute(selection, (entree))
    con.commit()
    con.close()

def seuil_commande (stock,seuil_recomp,nom): #stock, nom et seuil_recomp sont des listes et si les stock sont sup au seuil, la colonne a_commander de la pièce passe à 1

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    taille=len(stock)
    for i in range (0,taille):
        print (seuil_recomp[i])
        print (stock[i])
        try:
            seuil_recomp[i]=int(seuil_recomp[i])
        except:
            print ("non")
        else:
            if (stock[i]-seuil_recomp[i]<=0):
                colonne=["a_commander", "nom"]
                entree=[1, nom[i]]
                types=["int","str"]
                mise_a_jour_bdd("piece", colonne, entree, types)
    con.commit
    con.close

def tableau (base,colonne): #prend les infos d'une base, et les rentres dans un tableau avec tableau[0]= colonne[0], tableau[1]=colonne[1]...

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    tableau=[]*len(colonne)
    for i in colonne:
        selection= "SELECT " + i + " FROM " + base
        cur.execute(selection)
        listes=liste(cur.fetchall())
        tableau.append(listes)
    return tableau
