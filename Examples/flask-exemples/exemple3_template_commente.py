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
	contenu += "<a href='/template_get?prenom=toi'>Lien direct</a><br/><br/>" #hypertexte lien direct vers l'autre page (= vue) et definition par defaut de la variable prenom = toi avec la méthode template get

	contenu += "<form method='get' action='template_get'>" # active bouton envoyer
	contenu += "<input type='text' name='prenom' value=''>" #champ à remplir qui changera la valeur prise par 'prenom'
	contenu += "<input type='submit' value='Envoyer'>" #bouton envoyer
	contenu += "</form><br/>" #3x à la ligne

	return contenu;


@app.route('/template_get', methods=['GET'])
def template_html():
	return render_template('hello.html', prenom=request.args.get('prenom', '')) #render_template permet d'afficher la page html prise en argument (ici hello.html)
# cette page html a besoin de prenom pour fonctionner, c'est le deuxieme argument (voir ex2) (il est dispensable).

# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True, port=5678) #au fait on peut changer le port oklm si on veut, et le mode debug doit etre False une fois le site terminé
