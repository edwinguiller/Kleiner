from flask import Flask, url_for, request, render_template, redirect
from fonctions_logiques import *
from constantes import *
import sqlite3 as lite
import random

app = Flask(__name__)

# Une belle (Hyp'ss) page d'accueil avec un lien vers la partie Agilean et un vers la partie Agilog
@app.route('/')
def index():
    return render_template('accueil.html');

#La page Agilog
@app.route('/Agilog')
def agilog():
    return render_template('agiLog_accueil.html');


@app.route('/Agilog/Encours')
def encoursAlog(): #à faire
    return render_template('encours_alog.html')

@app.route('/Agilog/Encours/Declarer_kit', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def declarer_kit():

    contenu=""
    contenu += "<form method='get' action='Declarer_kit'>"
    contenu += "num kit "
    contenu += "<input type='text' name='num_kit' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    num_kite=request.args.get('num_kit','')
    #génération de l'id
    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT id FROM production")
    liste_id1 = cur.fetchall()
    liste_id2=[]
    for chaque in liste_id1:
        liste_id2.append(int(chaque[0]))
    if len(liste_id2)==0:
        newid=1
    else:
        newid=max(liste_id2)+1
    con.close()

    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    a=0
    d=cur.execute(" SELECT datetime('now')")
    if (num_kite!=""):
        d=cur.execute(" SELECT datetime('now')")
        cur.execute("INSERT INTO production('id', 'kit', 'fini','date') VALUES (?,?,?,?)", [newid ,num_kite ,1, d ])
    #con.commit()#enregistrer la requete de modification.
    cur.execute("SELECT id, kit, fini, date FROM Production;")
    liste = cur.fetchall()
    #
    for chaque in liste:
        contenu += "<br/>"
        contenu += str(chaque[0]) + " "
        contenu += str(chaque[1]) + " "
        contenu += str(chaque[2]) + " "
        contenu += str(chaque[3]) + " "
    con.close()

    return contenu;

@app.route('/Agilog/Encours/Aff_stock', methods=['GET']) #la page pour passer une commande
def commande():

    contenu = ""
    contenu += "Page de commande"
    contenu += "<br/> "
    contenu += "Vous allez passer " + request.args.get('nombre', 'une valeur par défaut de la req') + " commandes!"# juste un rappel du nombre de kit qu'on prend
    for i in range (0,request.args.get('nombre', 'une valeur par défaut de la req')):
        contenu += "bj"
    return contenu

#La page Initialisation
@app.route('/Agilog/Initialisation')
def initialisation ():
    return render_template('initialisation_alog.html')
    


@app.route('/Agilog/Initialisation/Ajout_piece', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def ajout_piece():
    # la demande du nom de la piece à rajouter et du stock à mettre
    contenu=""
    contenu += "<form method='get' action='Ajout_piece'>"
    contenu += "nom de la piece <br/>"
    contenu += "<input type='text' name='nom' value=''>"
    contenu += "<br/>"
    contenu += "stock de depart <br/>"
    contenu += "<input type='int' name='quantite' value=''>"
    contenu += "<br/>"
    contenu += "ton id <br/>"
    contenu += "<input type='text' name='id' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nome=request.args.get('nom','')
    quantitee=request.args.get('quantite','')
    ide=request.args.get('id','')

    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()

    #test si le stock est un entier si qlq chose est rentré
    if (nome!="" or quantitee!="" or ide!="" ):
        try:
            quantitee=int(quantitee)
        except:
            contenu += '<br/> le stock doit être un nombre entier'
        else:
            # on ajoute le nom l'id et le stock à la bdd
            con = lite.connect(cheminbdd)
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT nom FROM Piece;")
            testnom = cur.fetchall()
            test=[]
            for testnom in testnom:
                test.append(testnom[0]) # une liste pour ensuite voir si la piece demandé n'existe pas deja

            if (nome!="" and quantitee!= ""):
                if (nome in test):
                    contenu += "Cette piece existe deja"
                elif (nome!="" and quantitee>-1): #ajouter un createur d'id apres
                    cur.execute("INSERT INTO piece('nom', 'quantite', id) VALUES (?,?,?)", (nome,quantitee,ide))
                else:
                    contenu += (" Il faut un nom et une quantité positive")

    #delete
    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "<br/><br/> quel est le nom de la piece que tu veux tu supprimer? <br/>"
    contenu += "<input type='str' name='nomdel' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nomdele=request.args.get('nomdel','')
    if (nomdele != ""):
        cur.execute ("DELETE FROM 'piece' WHERE nom=?", [nomdele])

    cur.execute("SELECT nom, quantite, id FROM Piece;")
    liste = cur.fetchall()
    #
    for chaque in liste:
        contenu += "<br/>"
        contenu += str(chaque[0]) + " "
        contenu += str(chaque[1]) + " "
        contenu += str(chaque[2]) + " "

    #con.commit()
    con.close()

    return contenu; # LES PROGRAMMEURS a retoucher / separer  fonctions

@app.route('/Agilog/Initialisation/Gestion_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def gestion_stock():
    contenu=""

    #demande le nom de la piece, le seuil de recompletement, le stock de secu et le delai de reapro a changer en fournisseur
    contenu += "<form method='get' action='Gestion_stock'>"
    contenu += "quel est le nom de ta piece <br/>"
    contenu += "<input type='str' name='nom' value=''>"
    contenu += "<br/> <br/>"
    contenu += "quel est le seuil de recompletement <br/>"
    contenu += "<input type='int' name='seuil' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le stock de securite <br/>"
    contenu += "<input type='int' name='secu' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le delai de réapprovisionnement <br/>"
    contenu += "<input type='int' name='delai' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nome=request.args.get('nom','')
    seuile=request.args.get('seuil','')
    secue=request.args.get('secu','')
    delaie=request.args.get('delai','')
    #test si ce sont bien des entiers
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute ("SELECT nom FROM Piece;")

    test = cur.fetchall()# pour vérifier si le nom existe bien
    test_nom=[]
    for tous in test:
        test_nom.append(tous[0])

    # si tout est bien rempli on met a jour la bdd
    if (nome!="" and seuile!="" and secue!="" and delaie!=""):
        try:
            seuile=int(seuile)
            secue=int(secue)
            delaie=int(delaie)
        except:
            contenu += '<br/> Les stocks de sécurité, les delais de réapprovisionnement et le seuils de recompletement doivent être des nombres entier'
        else:
            if (seuile<0 or secue<0 or delaie<0):
                contenu += " <br/> Les nombres doivent être supérieur à 0"
            elif (nome not in test_nom):
                contenu += '<br/> le nom n est pas dans la liste des pieces <br/>'
            else:
                cur.execute("UPDATE Piece SET seuil_recomp=?, stock_secu=?, delai_reappro=? WHERE nom=?", [seuile,secue,delaie,nome])
    #con.commit()#enregistrer la requete de modification.
    # ceci est juste un affichage basique de la bdd, a remplacer par un vrai tableau
    cur.execute("SELECT nom, quantite, id, seuil_recomp, stock_secu, delai_reappro FROM Piece;")
    liste = cur.fetchall()
    for chaque in liste:
        contenu += "<br/>"
        contenu += str(chaque[0]) + " "
        contenu += str(chaque[1]) + " "
        contenu += str(chaque[2]) + " "
        contenu += str(chaque[3]) + " "
        contenu += str(chaque[4]) + " "
        contenu += str(chaque[5])
    con.close()
    #contenu += render_template('affichage_personnes.html', personnes = lignes)#une fonction html pour afficher un tableau

    return contenu;

@app.route('/Agilog/Initialisation/Code_kit', methods=['GET', 'POST'])
def code_kit():
	contenu=""
	contenu += "<a href='/accueil/agilog/initialisation/'>retour à la page précédente</a><br/>"
	contenu += "<br/>"
	contenu += "Kit"
	contenu += "<br/>"
	return(ajouter_piece_dans_kit())
#La page pour Agilean
@app.route('/Agilean')
def agilean():
    return render_template('agiLean_accueil.html');

@app.route('/Agilean/Reception')
def receptkit():
    return render_template('recept_stock_alean.html')+"</br> page non faite"



# se lance avec http:

#//localhost:5678
if __name__ == '__main__':
    app.run(debug=True, port=5678)
