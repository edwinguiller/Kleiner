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

#La page pour Agilean avec une vision d'un historique des commandes, un lien vers une recherche de commande, un lien pour commander des kit
@app.route('/Agilean')
def Agilean():
#<br/>
    contenu = ""
    contenu += "<a href='/'>retour à la page d'accueil</a><br/>"#un retour a la page d'accueil
    contenu += "<br/> "
    contenu += "Page Agilean "
    contenu += "<br/> "
    contenu += "Combien voulez vous passer de commandes? "# une demande pour savoir combien de kit on veut commander et qui envois vrs la page commande
    contenu += "<form method='get' action='commande'>"
    contenu += "<input type='int' name='nombre' value=''>"
    contenu += "<input type='submit' value='passer commande'>"
    return contenu;

#La page Agilog avec un historique des commandes, et une vision des commandes en cours avec la possibilité de dire qu'on a traité la commande et qu'on a fini de préparer
@app.route('/Agilog')
def Agilog():
#<br/>
    contenu = ""
    contenu += "<a href='/'>retour à la page d'accueil</a><br/>"#un retour a la page d'accueil
    contenu += "<br/> "
    contenu += "Page Agilog"
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
