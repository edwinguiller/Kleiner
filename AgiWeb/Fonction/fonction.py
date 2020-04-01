from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite

app = Flask(__name__)
#créer les stocks initiaux
@app.route('/')
def index():

    contenu = ""
    contenu += "<form method='get' action='ajout_piece'>"
    contenu += "prenom <br/>"
    contenu += "<input type='text' name='prenom' value=''>"
    contenu += "<br/>"
    contenu += "nom <br/>"
    contenu += "<input type='text' name='nom' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"
    contenu += "<a href='/accueil/agilog/initialisation/ajout_piece'>Lien direct</a><br/><br/>"
    return contenu;


@app.route('/accueil/agilog/initialisation/ajout_piece', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def ajout_piece():
    contenu=""
    contenu += "<form method='get' action='ajout_piece'>"
    contenu += "prenom <br/>"
    contenu += "<input type='text' name='prenom' value=''>"
    contenu += "<br/>"
    contenu += "nom <br/>"
    contenu += "<input type='text' name='nom' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    prenome=request.args.get('prenom','')
    nome=request.args.get('nom','')

    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    if (nome!=""):
        cur.execute("INSERT INTO personnes('nom', 'prenom') VALUES (?,?)", (nome,prenome))

    cur.execute("SELECT nom, prenom, role FROM personnes;")
    lignes = cur.fetchall()
    #con.commit()#enregistrer la requete de modification.
    con.close()
    contenu += render_template('affichage_personnes.html', personnes = lignes)

    return contenu;

@app.route('/accueil/agilog/initialisation/gestion_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def gestion_stock():
    contenu=""
    contenu += "quel est le nom de ta piece"
    contenu += "<input type='int' name='secu' value=''>"
    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "quel est le seuil de recommanda <br/>"
    contenu += "<input type='int' name='seuil' value=''>"
    contenu += "<br/>"
    contenu += "le stock de securite<br/>"
    contenu += "<input type='int' name='secu' value=''>"
    contenu += "le delai de réapprovisionnement<br/>"
    contenu += "<input type='int' name='delai' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"
    # a finir
    prenome=request.args.get('prenom','')
    nome=request.args.get('nom','')

    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    if (nome!=""):
		cur.execute("UPDATE piece SET seuil_recomp=?, stock_secu=?, delai_reappro=? WHERE nom=?", (nome,prenome))
		cur.execute("UPDATE employe SET salaire=? WHERE id=?",[salaire,ide])
		cur.execute("SELECT nom, prenom, role FROM personnes;")
    lignes = cur.fetchall()
    #con.commit()#enregistrer la requete de modification.
    con.close()
    contenu += render_template('affichage_personnes.html', personnes = lignes)

    return contenu;
if __name__ == '__main__':
    app.run(debug=True, port=5678)
