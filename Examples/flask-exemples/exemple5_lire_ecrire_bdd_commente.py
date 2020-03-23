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
	contenu += "<a href='/afficher_personnes'>Afficher les personnes</a><br/>"
	contenu += "<a href='/ajouter_personne'>Ajouter une personne</a><br/><br/>"

	return contenu;

@app.route('/afficher_personnes', methods=['GET'])
def afficher_personnes():

	con = lite.connect('/Users/Nathan/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db') #attention chez toi c'est pas rangé au meme endroit
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("SELECT nom, prenom, role FROM personnes")
	lignes = cur.fetchall()
	con.close()
	return render_template('affichage_personnes.html', personnes = lignes)

@app.route('/ajouter_personne', methods=['GET', 'POST']) #GET c pour obtenir une info, POST pour en donner une. C'est les methodes html qui vont etre utilsees dans la vue. Faut les declarer sinon pas autorisees a etre employees
def ajouter_personne():

	if not request.method == 'POST': #ce if la on voit pas trop a quoi ça sert, mais c'est utile par secu au cas ou d'autres methodes sont utilisees je crois.
		return render_template('formulaire_personne.html', msg = "", nom = "", prenom = "", role = 0)
	else:
		nom = request.form.get('nom', '') #on rentre les champs quoi
		prenom = request.form.get('prenom','')
		role = request.form.get('role', 0, type=int) #0 par defaut et on oblige à etre un nb entier (cf les fichiers html de pk ça affiche autre chose)

		if (nom != "" and prenom != "" and role > 0 and role < 4): #en gros si on a rempli tous les champs
			con = lite.connect('/Users/Nathan/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db') #bon la c'est du sql comme en tp
			con.row_factory = lite.Row
			cur = con.cursor()
			cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom,prenom,role))
			con.commit()#enregistrer la requete de modification.
			con.close()
			return redirect(url_for('afficher_personnes'))
		else:
			return render_template('formulaire_personne.html', msg = "Mauvaise saisie !", nom = "", prenom = "", role = 0) #si tous les champs sont pas remplis on reinitialise les variables et on revient à la meme page et on affiche message d'erreur


# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True, port=5678)
