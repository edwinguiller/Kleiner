# coding: utf-8
import sqlite3 as lite
import time

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

def test_rien(entree) # test si les entree ne sont pas vide renvois
