from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
import time

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
from fonctions_logiques import *

def modif_kit(kit_a_modif,piece_a_ajouter,quantite):
	contenu=""
	con = lite.connect('AgiWeb_BDD.db')
	con.row_factory = lite.Row
	cur=con.cursor()
	cur.execute("SELECT nom FROM piece;")
	pieces=cur.fetchall()#variable pour le menu déroulant pour le choix des pieces
	cur.execute("SELECT id_kit FROM kit wHERE nom_kit=?;",[kit_a_modif])#car dans la base compo_kit, kit correspond à des id
	kit_a_modifier=liste(cur.fetchall())#variable pour travailler dans la base compo_kit
	cur.execute("SELECT piece FROM compo_kit WHERE kit=?;",[kit_a_modifier[0]])
	piece_du_kit=liste(cur.fetchall())#cette liste nous permet de vérifier que la nouvelle pièce à ajouter n'est pas déjà présente
	#Si on veut supprimer une piece du kit
	if piece_a_ajouter[0]:
		cur.execute("DELETE FROM compo_kit WHERE kit=?,piece=?;",[kit_a_modifier[0],piece_a_ajouter[1]])
	#Si on veut ajouter une piece au kit
	else:
		if piece_a_ajouter not in piece_du_kit:#la pièce n'est pas présente dans le kit
			if quantite[1]==True:#la quantite est bonne donc on ajoute la piece simplement au kit
				cur.execute("INSERT INTO compo_kit(kit,piece,quantite) VALUES (?,?,?);",[kit_a_modifier[0],piece_a_ajouter[1],quantite[0]])
			else:#la quantite entrée n'est pas bonne
				print("la quantite n'est pas bonne")
		else:#la piece est présente dans le kit, on modifie donc juste la quantite
			cur.execute("UPDATE compo_kit SET quantite=? WHERE kit=?,piece=?;",[quantite[0],kit_a_modifier[0],piece_a_ajouter[1]])





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

    con = lite.connect('/Users/Nathan/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
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

    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "quel est le nom de ta piece <br/>"
    contenu += "<input type='str' name='nom' value=''>"
    contenu += "<br/> <br/>"
    contenu += "quel est le seuil de recommanda <br/>"
    contenu += "<input type='int' name='seuil' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le stock de securite <br/>"
    contenu += "<input type='str' name='secu' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le delai de réapprovisionnement <br/>"
    contenu += "<input type='str' name='delai' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nome=request.args.get('nom','')
    seuile=request.args.get('seuil','')
    secue=request.args.get('secue','')
    delaie=request.args.get('delai','')

    con = lite.connect('/Users/Nathan/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()

    if (nome!="" or seuile!="" or secue!="" or delaie!=""):
        try:
            seuile=int(seuile)
        except:
            contenu += 'gros c est pas un nombre'
        else:
            cur.execute("SELECT nom, prenom, role FROM personnes;")
            test = cur.fetchall()
            L=[]
            for test in test:
                L.append(test[1])
            if (nome=="" and seuile=="" and secue=="" and delaie==""):
                contenu += ""
            elif (nome=="a" or nome in L):
                #for row in cur.execute('SELECT date, num_facture FROM achat WHERE fournisseur=? ORDER BY date ASC',[fournisseur1]):
                contenu += " <br/> c'est pas bon"
            else:
                cur.execute("UPDATE personnes SET role=? WHERE nom=?", [seuile,nome])

    #delete
    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "<br/>quel est le nom de ta piece <br/>"
    contenu += "<input type='str' name='nomdel' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nomdele=request.args.get('nomdel','')
    cur.execute ("DELETE FROM 'personnes' WHERE nom=?", [nomdele])
    # fin du delete

    cur.execute("SELECT nom, prenom, role FROM personnes;")
    lignes = cur.fetchall()
    #con.commit()#enregistrer la requete de modification.
    con.close()
    contenu += render_template('affichage_personnes.html', personnes = lignes)

    return contenu;

@app.route('/accueil/agilog/en_cours/aff_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def aff_stock():

    contenu=""

    contenu += "<form method='get' action='aff_stock'>"
    contenu += "quel est le nom de ta piece <br/>"
    contenu += "<input type='str' name='nom' value=''>"
    contenu += "<br/> <br/>"
    contenu += "combien faut il en commender <br/>"
    contenu += "<input type='int' name='nb' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"
    nome=request.args.get('nom','')
    nbe=request.args.get('nb','')

    con = lite.connect('/Users/Nathan/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT delai_reappro, quantite FROM piece WHERE nom=?;", (nome))
    donne = cur.fetchall()
    quantitee= donne[1]+ nbe
    delai=donne[0]
    time.sleep(delai)
    cur.execute("UPDATE piece SET quantite=? WHERE nom=?", [quantitee,nome])
    #con.commit()#enregistrer la requete de modification.
    con.close()

    return contenu

if __name__ == '__main__':
    app.run(debug=True, port=5678)
