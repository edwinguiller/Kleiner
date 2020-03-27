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
    contenu += "<a href='/Agilog'>Initialisation</a><br/>"#lien vers l'initialisation
    contenu += "<a href='/Agilog'>Commande en cours</a><br/>" #lien vers les commandes en cours    

    return contenu;

#La page Initialisation
@app.route('/Initialisation')
def Initialisation ():
	
    contenu = ""
    contenu += "<a href='/'>retour à la page précédente</a><br/>"#un retour a la page d'accueil
    contenu += "<br/> "
    contenu += "Initialisation"
    contenu += "<br/> "
    contenu += "<a href='/Initialisation'>Stock</a><br/>"#lien vers le stock initial
    contenu += "<a href='/Initialisation'>Code kit</a><br/>" #lien vers les Code kit
    contenu += "<a href='/Initialisation'>Gestion stocks</a><br/>" #lien vers la gestion des stock
    
    return contenu;

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


# se lance avec http:

#//localhost:5678
if __name__ == '__main__':
    app.run(debug=True, port=5678)
