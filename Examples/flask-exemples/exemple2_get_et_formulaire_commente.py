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
@app.route('/') #en argument, c'est le chemin dans la barre de recherche pour aller dans la page de la fonction juste dessous (ici index, ou page d'accueil)
# '/' veut dire que c'est direct le lien (donc 127.0.0.1 pour nous)
def index():

	contenu = "" #on s'assure que contenu soit une chaine de caractère vide
	contenu += "<a href='/hello_get?prenom=toi'>Lien direct</a><br/><br/>" #cree variable dynamique 'prenom' qui de base prend 'toi' puis va à la ligne

	contenu += "<form method='get' action='hello_get'>" #permet au bouton envoyer et champ de fonctionner
	contenu += "<input type='text' name='prenom' value=''>" #ajoute juste un champ d'ecriture
	contenu += "<input type='submit' value='Envoyer'>" #bouton Envoyer (non fonctionnel)
	contenu += "</form><br/><br/>" #saut de ligne 2 fois (</form> = <br/><br/>)
	contenu += "ça bien sauté 2 lignes"

	return contenu #faut bien que la fonction renvoie un truc pour l'afficher ;)

# une page avec du texte dynamique envoyé par HTTP/GET
@app.route('/hello_get', methods=['GET']) #ici le nom de la page varie selon ce qu'ion a entré plus haut. methods=['GET'] renvoie +/- l'entrée
def hello_get_prenom():

	contenu = ""
	contenu += "<a href='/'>retour à l'index</a><br/><br/>" #crée un lien hypertexte puis saut de ligne
	contenu += "Hello, " + request.args.get('prenom', 'une valeur par défaut de la req') + " !" #request.args.get prend un dictionnaire (ou bdd)
#en agrgument. Ducou, le 'une valeur...req' c'est juste pour dire qu'on peut recup autre chose je crois

	return contenu

# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True, port=5678)
