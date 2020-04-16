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
	contenu += "<a href='/afficher_personnes'>Affichage des personnes de la BDD</a><br/><br/>"
	return contenu;


@app.route('/afficher_personnes', methods=['GET'])
def afficher_personnes():

	con = lite.connect('/Users/baba/Pictures/Kleiner/Kleiner/Examples/flask-exemples/exemples.db') #tu dis à quelle bdd tu te connectes
	con.row_factory = lite.Row #truc pour que le lien bdd-python fonctionnel
	cur = con.cursor() #placer le 'cuseur' de la bdd pret à recevoir des requetes
	cur.execute("SELECT nom, prenom, role FROM personnes;") #executer la requete sql
	lignes = cur.fetchall() #renvoyer le resultat sous forme d'array dans la variable 'lignes'. fecthall affiche tout, il existe aussi fetchone() (un seul)
	con.close() #je veux plus recevoir de requetes (c'est une scurite quoi...)
	return render_template('affichage_personnes.html', personnes = lignes) #comme d'hab

# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True, port=5678)
