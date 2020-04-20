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

def ajouter_piece_dans_kit (x=0):
    contenu += "<a href='/accueil/agilog/initialisation/'>retour à la page précédente</a><br/>"
    contenu += "<br/>"
    contenu += "Kit"
    contenu += "<br/>"
    if x==0 :
        #on crée un id
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT id FROM kit;")
        ide = creer_id(liste(cur.fetchall()))
        con.close()
        #On choisit et vérifier le nom du kit
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom FROM piece;")
        base=liste(cur.fetchall())
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_kit' value=''>"
        nom_kit=str(request.args.get('nom_kit',''))
        c=compare_nom(nom_kit,base)
        if c:
			#le nom du kit est déjà existant, on revient au départ
			contenu += "<br/>"
			contenu += "Erreur le nom existe déjà"
			contenu += "<br/>"
			contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
			contenu += "<br/>"
			time.sleep(5)
			return(ajouter_piece_dans_kit())
		else:
			#le nom est bon, on crée le kit dans la base kit
			cur.execute("INSERT INTO kit('id_kit', 'nom_kit') VALUES (?,?)", (ide,nom))
			return(ajouter_piece_dans_kit(ide))
    #Maintenant que le kit est créé on va le modifier
    else:
        contenu += "<br/>"
        contenu += "Entrer le nom puis la quantite de pièce"
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_piece' value=''>"
        contenu += "<input type='str' name='quantite' value=''>"
        contenu += "<input type='submit' value='Valider'>"
        nom_piece=str(request.args.get('nom_piece',''))
        quantite=request.args.get('quantite','')
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom FROM piece")
        ligne=liste(cur.fetchall())
        c=compare_nom(nom_piece,ligne)
        if c :
			#le nom est existe
			try:
				quantite=int(quantite)
				quantite>0
			except:
				#la quantite n'est pas bonne
				contenu += "<br/>"
				contenu += "Erreur la quantite est n'est pas bonne"
				contenu += "<br/>"
				contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
				contenu += "<br/>"
				time.sleep(5)
				return(ajouter_piece_dans_kit(x))
			else:
				#la quantité est un entier positif
				con = lite.connect(cheminbdd)
				con.row_factory = lite.Row
				cur=con.cursor()
				cur.execute("INSERT INTO compo_kit('kit', 'piece','quantite') VALUES (?,?,?)", (x,nom_piece,quantite))#On insert la nouvelle piece dans le kit
		else:
			#le nom de la pièce n'est pas bon
			contenu += "<br/>"
			contenu += "Erreur la pièce n'existe pas"
			contenu += "<br/>"
			contenu += "on recommence l'enregistrement de cette pièce ensemble mon chou dans quelques secondes"
			contenu += "<br/>"
			time.sleep(5)
			return(ajouter_piece_dans_kit(x))
		#On affiche la composition du kit
		con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT kit, piece, quantite FROM compo_kit")
        lignes=cur.fetchall()
        con.close()
        contenu += render_template('affichage_personnes.html', personnes = lignes)


>>>>>>> c79d95d98be4fce91b05071a2b51be92414ca68b

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

     # creation de l'id
    #con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    #con.row_factory = lite.Row
    #cur = con.cursor()
    #cur.execute("SELECT id FROM piece")
    #liste_id1 = cur.fetchall()
    #liste_id2=[]
    #for chaque in liste_id1:
    #    liste_id2.append(chaque[0])
    #taille=len(liste_id2)
    #print (liste_id2)
    #if taille==0:
    #    ide=1
    #else:
    #    ide=max(liste_id2)+1
    #con.close()

if __name__ == '__main__':
    app.run(debug=True, port=5678)
