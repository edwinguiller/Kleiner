from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
import random

app = Flask(__name__)

# Une belle (Hyp'ss) page d'accueil avec un lien vers la partie Agilean et un vers la partie Agilog
@app.route('/')
def index():

    contenu = ""
    contenu = "Page d'accueil <br/><br/>"
    contenu += "<a href='/Agilean'>Page Agilean</a><br/>" #lien vers Agilean
    contenu += "<a href='/Agilog'>Page Agilog</a>" # lien vers Agilog
    return contenu;

#La page pour Agilean
@app.route('/Agilean')
def Agilean():

    contenu = ""
    contenu = "Accueil Agilean <br/><br/>"
    contenu += "<a href='/'>retour à la page précédente</a><br/>"#un retour a la page d'accueil
    contenu += "<a href='/Agilean'>valider la réception</a><br/>" #lien vers la validation de la réception

    return contenu;

#La page Agilog
@app.route('/Agilog')
def Agilog():
#<br/>
    contenu = ""
    contenu += "<a href='/'>retour à la page précédente</a><br/>"#un retour a la page d'accueil
    contenu += "<br/> "
    contenu += "Page Agilog"
    contenu += "<br/> "
    contenu += "<a href='/Initialisation'>Initialisation</a><br/>"#lien vers l'initialisation
    contenu += "<a href='/Commande_en_cours'>Commande en cours</a><br/>" #lien vers les commandes en cours

    return contenu;

#La page Initialisation
@app.route('/Initialisation')
def Initialisation ():

    contenu = ""
    contenu += "<a href='/'>retour à la page précédente</a><br/>"#un retour a la page d'accueil
    contenu += "<br/> "
    contenu += "Initialisation"
    contenu += "<br/> "
    contenu += "<a href='/accueil/agilog/initialisation/ajout_piece'>Stock</a><br/>"#lien vers le stock initial
    contenu += "<a href='/Initialisation'>Code kit</a><br/>" #lien vers les Code kit
    contenu += "<a href='/Initialisation'>Gestion stocks</a><br/>" #lien vers la gestion des stock


    return contenu;

#

#La page pour passer une commande
@app.route('/commande', methods=['GET'])
def commande():

    contenu = ""
    contenu += "Page de commande"
    contenu += "<br/> "
    contenu += "Vous allez passer " + request.args.get('nombre', 'une valeur par défaut de la req') + " commandes!"# juste un rappel du nombre de kit qu'on prend
    for i in range (0,request.args.get('nombre', 'une valeur par défaut de la req')):
        contenu += "bj"
    return contenu

@app.route('/accueil/agilog/initialisation/ajout_piece', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def ajout_piece():
    contenu=""
    contenu += "<form method='get' action='ajout_piece'>"
    contenu += "nom de la piece <br/>"
    contenu += "<input type='text' name='nom' value=''>"
    contenu += "<br/>"
    contenu += "stock de depart <br/>"
    contenu += "<input type='int' name='quantite' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nome=request.args.get('nom','')
    quantitee=request.args.get('quantite','')

    if (nome!="" or quantitee!="" ):
        try:
            seuile=int(quantitee)
        except:
            contenu += '<br/> le stock doit être un nombre entier'

    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    if (nome!="" and quantitee>0): #ajouter test si nome n existe pas deja
        cur.execute("INSERT INTO piece('nom', 'quantite') VALUES (?,?)", (nome,quantitee))

    cur.execute("SELECT nom, quantite FROM piece;")
    lignes = cur.fetchall()
    con.commit()
    con.close()
    contenu += render_template('affichage_personnes.html', piece = lignes)#creer une fonction pour afficher les pieces deja existante

    return contenu;

@app.route('/accueil/agilog/initialisation/gestion_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def gestion_stock():
    contenu=""

    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "quel est le nom de ta piece <br/>"
    contenu += "<input type='str' name='nom' value=''>"
    contenu += "<br/> <br/>"
    contenu += "quel est le seuil de recommanda <br/>"
    contenu += "<input type='str' name='seuil' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le stock de securite <br/>"
    contenu += "<input type='str' name='secu' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le delai de réapprovisionnement <br/>"
    contenu += "<input type='str' name='delai' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"
    # a finir
    nome=request.args.get('nom','')
    seuile=request.args.get('seuil','')
    secue=request.args.get('secue','')
    delaie=request.args.get('delai','')

    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    if (nome=="" and seuile=="" and secue=="" and delaie==""):
        contenu += ""
    elif (nome=="a"):
        contenu += " <br/> c'est pas bon"
    else:
        cur.execute("UPDATE personnes SET prenom=? WHERE nom=?", [seuile,nome])
    cur.execute("SELECT nom, prenom, role FROM personnes;")
    lignes = cur.fetchall()
    #con.commit()#enregistrer la requete de modification.
    con.close()
    contenu += render_template('affichage_personnes.html', personnes = lignes)

    return contenu;
# se lance avec http:

#//localhost:5678
if __name__ == '__main__':
    app.run(debug=True, port=5678)
