from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite

# ------------------
# application Flask
# ------------------

app = Flask(__name__)

# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------

# une page index avec des liens vers les différentes pages d'exemple d'utilisation de Flask
@app.route('/')
def index():

    contenu = ""
    contenu += "<a href='/afficher_personnes'>Affichage des personnes de la BDD dont le prenom commence par la lettre </a><br/><br/>"
    contenu += "<form method='get' action='affichage_personnes_dont_la_premiere_lettre_est'>"
    contenu += "<input type='text' name='baba' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"
    return contenu;


@app.route('/afficher_personnes', methods=['GET'])
def afficher_personnes():

    con = lite.connect('exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT nom, prenom, role FROM personnes WHERE prenom LIKE 'A%'")
    lignes = cur.fetchall()
    con.close()
    return render_template('affichage_personnes.html', personnes = lignes)
@app.route('/affichage_personnes_dont_la_premiere_lettre_est', methods=['GET'])
def affichage_personnes_dont_la_premiere_lettre_est():
    contenu = ""
    contenu += "Hello, " + request.args.get('baba', 'une valeur par défaut de la req') + " !"

    contenu += "<a href='/'>retour à l'index</a><br/><br/>"
    con = lite.connect('exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()

    jeje=request.args.get('baba')
    contenu += jeje
    cur.execute("SELECT nom, prenom, role FROM personnes WHERE prenom LIKE 'jeje%'")
    lignes = cur.fetchall()
    con.close()
    return render_template('affichage_personnes.html', personnes = lignes)


    return contenu
# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=5678)
