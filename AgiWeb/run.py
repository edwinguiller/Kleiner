from flask import Flask, url_for, request, render_template, redirect
from fonctions_logiques import *
from constantes import *
import sqlite3 as lite
import random

app = Flask(__name__)

# Une belle (Hyp'ss) page d'accueil avec un lien vers la partie Agilean et un vers la partie Agilog
@app.route('/')
def index():
    return render_template('accueil.html');

#La page Agilog
@app.route('/Agilog')
def agilog():
    return render_template('agiLog_accueil.html');


@app.route('/Agilog/Encours')
def encoursAlog(): #à faire
    return render_template('encours_alog.html')

@app.route('/Agilog/Encours/Declarer_kit', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def declarer_kit():

    contenu = ""
    contenu += "<form method='get' action='declarer_kit'>"
    contenu += "num kit "
    contenu += "<input type='text' name='num_kit' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    num_kite=request.args.get('num_kit','')
    #génération de l'id
    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT id_vente FROM production")
    liste_id1 = cur.fetchall()
    liste_id2=[]
    for chaque in liste_id1:
        liste_id2.append(int(chaque[0]))
    if len(liste_id2)==0:
        newid=1
    else:
        newid=max(liste_id2)+1
    con.close()

    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    if (nome!=""):
        cur.execute("INSERT INTO production('id_vente', 'nom_kit', 'fini') Value (?,?,?)", (newid,num_kite,1))
    con.commit()#enregistrer la requete de modification.
    con.close()

    return contenu;

@app.route('/Agilog/Encours/Aff_stock', methods=['GET']) #la page pour passer une commande
def commande():

    contenu = ""
    contenu += "Page de commande"
    contenu += "<br/> "
    contenu += "Vous allez passer " + request.args.get('nombre', 'une valeur par défaut de la req') + " commandes!"# juste un rappel du nombre de kit qu'on prend
    for i in range (0,request.args.get('nombre', 'une valeur par défaut de la req')):
        contenu += "bj"
    return contenu

#La page Initialisation
@app.route('/Agilog/Initialisation')
def initialisation ():
    return render_template('initialisation_alog.html')

@app.route('/Agilog/Initialisation/ajout_piece', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def ajout_piece():

    #variable message :
    err_quant = ''
    msg=''

    # affichage des pièces présente
    con = lite.connect('AgiWeb_BDD.db') #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT id_piece, nom, quantite FROM piece")
    liste_id = cur.fetchall()
    nome=request.form.get('nom','')
    quantitee=request.form.get('quantite','')
    ide = request.form.get('ide','')
    con.close()


    #test si le stock est un entier si qlq chose est rentré
    if (nome!="" or quantitee!="" ):
        try:
            quantitee=int(quantitee)
        except:
            err_quant = 'le stock doit être un nombre entier'
        else:
            # on ajoute le nom l'id et le stock à la bdd
            err_quant = ''
            con = lite.connect('AgiWeb_BDD.db')
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT nom FROM Piece")
            testnom = cur.fetchall()
            test=[]
            for testnom in testnom:
                test.append(testnom[0]) # une liste pour ensuite voir si la piece demandé n'existe pas deja

            if (nome!="" and quantitee!= ""):
                if (nome in test):
                    msg = "Cette piece existe deja"
                elif (nome!="" and quantitee>=0): #ajouter un createur d'id apres
                    cur.execute("INSERT INTO piece('nom', 'quantite', 'id_piece') VALUES (?,?,?)", (nome,quantitee,ide))
                    msg = ''
                    con.close()
                else:
                    msg += (" Il faut un nom et une quantité positive")
                #return redirect(url_for('ajout_piece'))

    nomdele=request.args.get('nomdel','')
    con = lite.connect('AgiWeb_BDD.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute ("DELETE FROM 'piece' WHERE nom=?", [nomdele])

    # a modifier, l'affichage des pieces
    cur.execute("SELECT nom, quantite FROM piece;")
    liste_piece = cur.fetchall()
    con.commit()
    con.close()


    return render_template('ajout_piece.html', liste_id=liste_id, liste_piece=liste_piece , err_quant= err_quant, msg=msg); # LES PROGRAMMEURS a retoucher / separer  fonctions

@app.route('/Agilog/Initialisation/Gestion_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def gestion_stock():
    contenu=""

    #demande le nom de la piece, le seuil de recompletement, le stock de secu et le delai de reapro a changer en fournisseur
    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "quel est le nom de ta piece <br/>"
    contenu += "<input type='str' name='nom' value=''>"
    contenu += "<br/> <br/>"
    contenu += "quel est le seuil de recompletement <br/>"
    contenu += "<input type='int' name='seuil' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le stock de securite <br/>"
    contenu += "<input type='int' name='secu' value=''>"
    contenu += "<br/> <br/>"
    contenu += "le delai de réapprovisionnement <br/>"
    contenu += "<input type='int' name='delai' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    nome=request.args.get('nom','')
    seuile=request.args.get('seuil','')
    secue=request.args.get('secue','')
    delaie=request.args.get('delai','')
    #test si ce sont bien des entiers
    try:
        seuile=int(seuile)
        secue=int(secue)
        delaie=int(delaie)
    except:
        contenu += '<br/> Les stocks de sécurité, les delais de réapprovisionnement et le seuils de recompletement doivent être des nombres entier'
    else:
        con = lite.connect(cheminbdd)
        con.row_factory = lite.Row
        cur = con.cursor()

        # si tout est bien rempli on met a jour la bdd
        if (nome=="" and seuile=="" and secue=="" and delaie==""):
            contenu += ""
        elif (seuile<0 or secue<0 or delaie<0 or nome==""):
            contenu += " <br/> Les nombres doivent être supérieur à 0"
        else:
            cur.execute("UPDATE Piece SET seuil_recomp=?, stock_secu=?, delai_reappro=? WHERE nom=?", [seuile,secue,delaie,nome])
    cur.execute("SELECT nom, id_piece, quantite, seuil_recomp, stock_secu, delai_reappro FROM piece;")
    lignes = cur.fetchall()
    #con.commit()#enregistrer la requete de modification.
    con.close()
    contenu += render_template('affichage_personnes.html', personnes = lignes)#une fonction html pour afficher un tableau

    return contenu;

@app.route('/Agilog/Initialisation/Code_kit', methods=['GET', 'POST'])
def code_kit():
    contenu=""
    contenu += "<a href='/accueil/agilog/initialisation/'>retour à la page précédente</a><br/>"
    contenu += "<br/>"
    contenu += "Kit"
    contenu += "<br/>"
    contenu += "<form method='get' action='code_kit'>"
    contenu += "<input type='str' name='Code_article' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"
    contenu += "<br/>"
    contenu +="Liste des pièces du Kit"
    contenu +="<br/>"

    code=request.args.get('Code_article','')
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur=con.cursor()
    cur.execute("SELECT role FROM personnes;")
    lignes = cur.fetchall()
    if code in lignes  or code=='':
        contenu += "<br/>"
        contenu += "Erreur le code existe déjà"
        contenu += "<br/>"
    else :
        contenu += "<br/>"
        contenu += "Entrer le nom puis la quantite de pièce"
        contenu += "<br/>"
        contenu += "<form method='get' action='code_kit'>"
        contenu += "<input type='str' name='nom_piece' value=''>"
        contenu += "<input type='str' name='quantite' value=''>"
        contenu += "<input type='submit' value='Valider'>"
        contenu += "<input type='submit' value='Ajouter piece'>"
    contenu += render_template('affichage_personnes.html', personnes = lignes)
    return contenu #LES PROGRAMMEURS pas fait

#La page pour Agilean
@app.route('/Agilean')
def agilean():
    return render_template('agiLean_accueil.html');

@app.route('/Agilean/Reception')
def receptkit():
    return render_template('recept_stock_alean.html')+"</br> page non faite"



# se lance avec http:

#//localhost:5678
if __name__ == '__main__':
    app.run(debug=True, port=5678)
