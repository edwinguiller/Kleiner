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
    if x==0 or contenu=="":
        contenu += "<a href='/accueil/agilog/initialisation/'>retour à la page précédente</a><br/>"
        contenu += "<br/>"
        contenu += "Kit"
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='Code_article' value=''>"
        contenu += "<input type='submit' value='Envoyer'>"
        code=int(request.args.get('Code_article',''))
        con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT role FROM personnes;")#à modifier
        lignes = cur.fetchall()
        if code in lignes  or code=='':
            contenu += "<br/>"
            contenu += "Erreur le code existe déjà"
            contenu += "<br/>"
            return (ajouter_piece_dans_kit(,contenu))#on recommence, attention comme ça, ça m'arche pas "type submit"
        else :
            con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
            con.row_factory = lite.Row
            cur=con.cursor()
            cur.execute("INSERT INTO ;")#à modifier, on crée le kit vierge
            return(ajouter_piece_dans_kit(code,contenu))
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
        nom_piece=str(request.args.get('nom_piece','')
        quantite=int(request.args.get('quantite','')
        con = lite.connect('/Users/Arthur LAUREILLE/Documents/GitHub/Kleiner/AgiWeb/Fonction/exemples.db')#à modifier
        con.row_factory = lite.Row
        cur=con.cursor()
        cur.execute("SELECT nom FROM piece")
        lignes=cur.fetchall()
        if nom_piece not in ligne or quantite=<0 :
            contenu += "<br/>"
            contenu += "Erreur la pièce n'existe pas ou la quantite est nulle"
            contenu += "<br/>"


#        cur.execute("UPDATE ;")#à modifier, on insert la nouvelle piece dans le kit

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

    con = lite.connect('/Users/Benjamin/Documents/GitHub/Kleiner/Examples/flask-exemples/exemples.db')
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
