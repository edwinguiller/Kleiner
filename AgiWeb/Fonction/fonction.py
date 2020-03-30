from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite

app = Flask(__name__)
#créer les stocks initiaux
@app.route('/')
def index():

    contenu = ""
    contenu += "<form method='get' action='template_get'>"
    contenu += "prenom <br/>"
    contenu += "<input type='text' name='prenom' value=''>"
    contenu += "<br/>"
    contenu += "nom <br/>"
    contenu += "<input type='text' name='nom' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    return contenu;


@app.route('/ajout_piece', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def ajout_piece():
    prenome=request.args.get('prenom')
    nome=request.args.get('nom')
    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("INSERT INTO personnes('nom', 'prenom') VALUES (?,?)", (nome,prenome))

    cur.execute("SELECT nom, prenom, role FROM personnes;")
    lignes = cur.fetchall()
    #con.commit()#enregistrer la requete de modification.
    con.close()

    return contenu;
if __name__ == '__main__':
    app.run(debug=True, port=5678)
