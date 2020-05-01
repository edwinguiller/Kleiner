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
        return(print([quantite,False]))
    else:
        if quantite>0:
            return(print([quantite,True]))
        else:
            return(print([quantite,False]))
quantite_bonne(0)


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

    if (test_rien(entree)==0):
        if test_types(entree,types)==0:
            cur.execute(selection, (entree))
    con.commit()
    con.close()

def seuil_commande (): #stock, nom et seuil_recomp sont des listes et si les stock sont inf au seuil, la colonne a_commander de la pièce passe à 1

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT quantite, seuil_recomp, nom FROM piece")
    d=tab(cur.fetchall())
    bdd=convert_dict(d,"quantite","seuil_recomp","nom")
    taille=len(bdd["quantite"])
    for i in range (0,taille):
        print (bdd["seuil_recomp"][i])
        print (bdd["quantite"][i])
        try:
            bdd["seuil_recomp"][i]=int(bdd["seuil_recomp"][i])
        except:
            print ("non")
        else:
            if (bdd["quantite"][i]-bdd["seuil_recomp"][i]>=0):
                colonne=["a_commander", "nom"]
                entree=[1, bdd["nom"][i]]
                types=["int","str"]
                mise_a_jour_bdd("piece", colonne, entree, types)
            elif (bdd["quantite"][i]-bdd["seuil_recomp"][i]<=0):
                colonne=["a_commander", "nom"]
                entree=[0, bdd["nom"][i]]
                types=["int","str"]
                mise_a_jour_bdd("piece", colonne, entree, types)
    con.commit()
    con.close()

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
def tab (listesql): #prend une liste sql et la transforme en tableau

    tt=[]
    for i in listesql:
        a=[]
        for j in i:
            a.append(j)
        tt.append(a)
    ttt=[0]*len(tt[0])
    for i in range (0,len(tt[0])):
        ttt[i]=[0]*len(tt)
    for i in range (0,len(tt[0])):
            for j in range (0,len(tt)):
                ttt[i][j]=tt[j][i]
    return(ttt)
def convert_dict(L,c1=None,c2=None,c3=None,c4=None,c5=None,c6=None,c7=None,c8=None): #ci colonnes, ce sont des strings
    D=dict()
    C=[c1,c2,c3,c4,c5,c6,c7,c8]
    for i in range(8):
        if type(C[i])==str:
            D[C[i]]=L[i]
    return D

def select_encours (): #selectionne les stocks en cours pour pouvoir ensuite les afficher
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT id_com as id, date,nom as nom,quantite, strftime('%s',date_arrivee)- strftime('%s',strftime('%H:%M:%S','now')) as timer from (SELECT id_com,nom,quantite,date,delai,strftime('%H:%M:%S',(SELECT commande.date FROM commande),delai) as date_arrivee from (SELECT piece.id as id_piece,piece.nom, piece.fournisseur, fournisseur.delai from piece join fournisseur ON piece.fournisseur==fournisseur.id) JOIN (SELECT commande.id as id_com,commande.date,compo_commande.piece,compo_commande.quantite from commande join compo_commande on commande.id==compo_commande.commande WHERE reception==0) ON id_piece==piece) ORDER by id_com;")
    b=cur.fetchall() #ajouté
    #d=tab(cur.fetchall())
    #b=convert_dict(d,"id","date","nom", "quantite","timer")
    con.close()

    return b

def select_stock_reel (): #selectionne les stocks reel pour pouvoir ensuite les afficher
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT id, nom, quantite, a_commander FROM piece")
    b=cur.fetchall() # ajouté
    #d=tab(cur.fetchall())

    #b=convert_dict(d,"id","nom","quantite", "a_commander")
    #for i in range (0,len(b["a_commander"])):
    #    if (b["a_commander"][i]==1):
    #        b["a_commander"][i]="OUI"
    #    elif (b["a_commander"][i]==0):
    #        b["a_commander"][i]="NON"
    #    else:
    #        b["a_commander"][i]="ERREUR"
    con.close()

    return b

def select_commande_fournisseur (fournisseur): #prend le fournisseur en lettre minuscule et("agigreen" ou "agipart") et renvoi les id, nom et quantité des pièces à commander du fournisseur
    #fonctionne uniquement si il y'a quelque chose dans la colonne à commander (0 ou 1) pour les 2 fournisseur mais pas si il y'a que des NULL, si il y a que des NULL c'est chiant faut que je fasse un test pour ca
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()

    if (transformation(fournisseur)=="agigreen"):
        fourniss=1
    elif (transformation(fournisseur)=="agipart"):
        fourniss=2
    else:
        return ERREUR
    cur.execute("SELECT id, nom, quantite FROM piece WHERE a_commander=? and fournisseur=?", [1,fourniss])
    a=cur.fetchall()
    if (a==[]):
        print ("il n y a rien")
        return a
    d=tab(a)
    b=convert_dict(d,"id","nom","quantite")
    con.close()

    return b

def passer__commande(commande): #prend en argument le dictionnaire commande avec les id des pieces, leurs nom et la quantite et créer la commande et la compo commande associé

    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    # générer id
    cur.execute ("SELECT id FROM commande")
    liste_id=(cur.fetchall())
    new_id=creer_id(liste_id)
    d=cur.execute(" SELECT datetime('now')")
    date=cur.fetchall()[0][0]
    # creation de la commande
    if (commande==[]):
        return
    cur.execute("INSERT INTO commande (id,date,reception) VALUES (?,?,?)", (new_id,date,0))
    for i in range (0,len(commande["id"])):
        cur.execute("INSERT INTO compo_commande(commande,piece,quantite) VALUES(?,?,?)", (new_id, commande["id"][i], commande["quantite"][i]))
    cur.execute("UPDATE fournisseur SET derniere_com=CURRENT_TIMESTAMP WHERE fournisseur.id==(SELECT fournisseur FROM commande JOIN (SELECT piece.fournisseur,compo_commande.commande, compo_commande.piece FROM compo_commande JOIN piece ON compo_commande.piece==piece.id) WHERE commande.id==?)", [new_id])
    con.commit()
    con.close()
    return

def valider_reception_commande(idcom): # prend en argumant l'id d une commande et la met recu et rajoute les pieces au stocks

    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur=con.cursor()
    cur.execute("UPDATE piece SET quantite = (SELECT nq FROM (SELECT piece,piece.quantite+quantite_com as nq FROM (SELECT commande.id, compo_commande.piece,compo_commande.quantite as quantite_com FROM commande JOIN compo_commande ON commande.id==compo_commande.commande WHERE commande.id==?) JOIN piece ON piece.id=piece ) WHERE piece.id==piece) WHERE (SELECT nq FROM (SELECT piece,piece.quantite+quantite_com as nq FROM (SELECT commande.id, compo_commande.piece,compo_commande.quantite as quantite_com FROM commande JOIN compo_commande ON commande.id==compo_commande.commande WHERE commande.id==?) JOIN piece ON piece.id=piece ) WHERE piece.id==piece) IS NOT NULL",[idcom,idcom])
    cur.execute("SELECT quantite FROM piece")
    print (tab(cur.fetchall()))
    cur.execute("UPDATE commande SET reception=? WHERE commande.id==?", [1,idcom])
    cur.execute("SELECT reception FROM commande")
    print (tab(cur.fetchall()))
    con.commit()
    con.close()
    return
