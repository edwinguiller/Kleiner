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


def ajouter_piece_dans_kit (x=0,contenu=""):
    contenu += "<a href='/accueil/agilog/initialisation/'>retour à la page précédente</a><br/>"
    contenu += "<br/>"
    contenu += "Kit"
    contenu += "<br/>"
    if x==0 or contenu=="":
        #on crée le Kit
        con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT id FROM kit;")#à modifier
        lignes1 = cur.fetchall()
        lignes2 = []
        for chaque in lignes1:
			lignes2.append(chaque[0])
		taille=len(lignes2)
		if taille==0:
			ide=1
		else:
			ide=max(lignes2)+1
		con.close()
        con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("INSERT INTO ;")#à modifier, on crée le kit vierge
        return(ajouter_piece_dans_kit(code,))
    else:
        contenu += "<br/>"
        contenu += "Vous etes entrain de créer le Kit n°"+str(x)
        contenu += "<br/>"
        contenu += "<br/>"
        contenu += "Entrer le nom puis la quantite de pièce"
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_piece' value=''>"
        contenu += "<input type='str' name='quantite' value=''>"
        contenu += "<input type='submit' value='Valider'>"
        nom_piece=str(request.args.get('nom_piece',''))
        quantite=request.args.get('quantite','')
        con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom FROM piece")
        lignes=cur.fetchall()
        if nom_piece not in ligne :
			try:
				quantite=int(quantite)
				quantite>0
			except:	
				contenu += "<br/>"
				contenu += "Erreur la quantite est n'est pas bonne"
				contenu += "<br/>"
				contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"#time.sleep()
				contenu += "<br/>"
				time.sleep(5)
				return(ajouter_piece_dans_kit(code,))
			else:
				con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
				con.row_factory = lite.Row
				cur=con.cursor()
				cur.execute("UPDATE ;")#à modifier, on insert la nouvelle piece dans le kit
		else:
			contenu += "<br/>"
			contenu += "Erreur la pièce n'existe pas"
			contenu += "<br/>"
			contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"#time.sleep()
			contenu += "<br/>"
			time.sleep(5)
			return(ajouter_piece_dans_kit(x,))	
			

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



    if (nome!="" or seuile!="" or secue!="" or delaie!=""):
        try:
            seuile=int(seuile)
        except:
            contenu += 'gros c est pas un nombre'
    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
    con.row_factory = lite.Row
    cur = con.cursor()
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

    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
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
