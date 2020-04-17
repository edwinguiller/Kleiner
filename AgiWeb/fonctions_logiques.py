# coding: utf-8
import sqlite3 as lite
from constantes import *
import time

def ajouter_piece(nome, quantitee, ide): # prend en argument  un nom une quantité et un id et les rajoute a la bdd piece apres avoir fait des test dessus+

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    contenu =''
    #test si le stock est un entier si qlq chose est rentré
    if (nome!="" or quantitee!="" or ide!="" ):
        try:
            quantitee=int(quantitee)
        except:
            contenu += '<br/> le stock doit être un nombre entier'
        else:
            # on ajoute le nom l'id et le stock à la bdd
            if (nome!="" and quantitee!= ""):
                if (testin('piece', 'nom', nome)==1 or testin('piece', 'id', ide)==1): # verifie si l'id ou le nom n'existent pas deja
                    contenu += "Cette piece existe deja"
                elif (nome!="" and quantitee>-1): #ajouter un createur d'id apres
                    cur.execute("INSERT INTO piece('nom', 'quantite', id) VALUES (?,?,?)", (nome,quantitee,ide))
                else:
                    contenu += (" Il faut un nom et une quantité positive")
    con.commit()
    con.close()
    return contenu

def delete (base, source, nom): #prend en argument une base (ex: piece), une colonne dans cette base (ex: nom) et supprime la ligne quand la valeur de la colonne vaut nomdele

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    suppr="DELETE FROM " + base + " WHERE " +source+ "=?"
    if (nom != ""):
        cur.execute (suppr, [nom])
    con.commit()
    con.close()

def testin (base, source, variable): # test si la variable est deja dans la bdd return 1 si il y'est et 0 si il n'y est pas
    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    selection="SELECT " + source + " FROM " + base + ";"
    cur.execute(selection)
    recuperer=cur.fetchall()
    test=[]
    for valeur in recuperer:
        test.append(valeur[0])
    if (variable in test):
        retour=1
    elif (variable not in test):
        retour=0
    else:
        return error
    return retour
