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
		contenu += "<form method='get' action='code_kit'>"
		contenu += "<input type='str' name='nom_kit"+str(i)+"' value=''>"
	contenu += "<input type='submit' value='Envoyer'>"
	return(contenu)
def recupere_interraction(n,contenu):
	L=[]
	for i in range(n):
		nom=str(request.args.get('nom_kit'+str(i),''))
		L.append(nom)
	return(L)
def ajouter_piece_dans_kit (x=0):
    if x==0 :
        #on sélectionne les id
        contenu =""
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT id FROM kit;")
        ids=liste(cur.fetchall())
        con.close()
        #On choisit et vérifier le nom du kit
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom_kit FROM kit;")
        base=liste(cur.fetchall())
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_kit' value=''>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='id_kit' value=''>"
        print(contenu)
        nom_kit=str(request.args.get('nom_kit',''))
        id_kit=str(request.args.get('id_kit',''))
        c=compare_nom(nom_kit,base)
        d=compare_nom(id_kit,ids)
        if c or d:#le nom du kit est déjà existant, on revient au départ
            contenu += "<br/>"
            contenu += "Erreur le nom existe déjà"
            contenu += "<br/>"
            contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
            return(ajouter_piece_dans_kit())
        else:
            #le nom est bon, on crée le kit dans la base kit
            cur.execute("INSERT INTO kit('id', 'nom_kit') VALUES (?,?)", (id_kit,nom_kit))
            return(ajouter_piece_dans_kit(id_kit))
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

def ajouter_piece(base, colonne, entree, types): # prend en argument  une base (ex: piece), les colonnes que l'on veut modifier (une liste ex: [id, nom...]), les entrées (valeurs) et le type de ces valeurs

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
    for i in range (0,taille):
        if (entree[i]==""):
            print ("ok boomer")
    #test si le stock est un entier si qlq chose est rentré
    #if (nome!="" or quantitee!="" or ide!="" ):
    #    try:
    #        quantitee=int(quantitee)
    #    except:
    #        contenu += '<br/> le stock doit être un nombre entier'
    #    else:
    #        # on ajoute le nom l'id et le stock à la bdd
    #        if (nome!="" and quantitee!= ""):
    #            if (testin('piece', 'nom', nome)==1 or testin('piece', 'id', ide)==1): # verifie si l'id ou le nom n'existent pas deja
    #                contenu += "Cette piece existe deja"
    #            elif (nome!="" and quantitee>-1): #ajouter un createur d'id apres
    #                cur.execute("INSERT INTO piece('nom', 'quantite', id) VALUES (?,?,?)", (nome,quantitee,ide))
    #            else:
    #                contenu += (" Il faut un nom et une quantité positive")
    #con.commit()
    #con.close()
    return contenu

def delete (base, colonne, entree): #prend en argument une base (ex: piece), une colonne dans cette base (ex: nom) et supprime la ligne quand la valeur de la colonne vaut nomdele

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    suppr="DELETE FROM " + base + " WHERE " +colonne+ "=?"
    if (entree != ""):
        cur.execute (suppr, [entree])
    con.commit()
    con.close()

def testin (base, colonne, entree): # test si la entree est deja dans la bdd return 1 si il y'est et 0 si il n'y est pas

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

#def test_rien(entree) #test si les entree ne sont pas vide renvois
