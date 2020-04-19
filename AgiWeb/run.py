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
@app.route('/Agilog/Initialisation/')
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

    if not request.method == 'POST':
        con.close()
        return render_template('ajout_piece.html',liste_id=liste_id, err_quant= "", msg="")
    else:
        nome = request.form.get('nome','')
        quantitee = request.form.get('quantitee','')
        ide = request.form.get('ide','')

        #test si le stock est un entier si qlq chose est rentré
        try:
            quantitee=int(quantitee)
            assert quantitee>=0
        except ValueError:
            con.close()
            return render_template('ajout_piece.html',liste_id=liste_id, err_quant= err_quant, msg='le stock doit être un nombre entier')
        except AssertionError :
            con.close()
            return render_template('ajout_piece.html',liste_id=liste_id, err_quant= "", msg="Il faut une quantité positive")

        if (nome!="" and quantitee!="" and ide!="" and quantitee>=0):
            # on ajoute le nom l'id et le stock à la bdd
            cur.execute("SELECT id_piece FROM Piece")
            testnom = cur.fetchall()
            test=[]
            for testnom in testnom:
                test.append(testnom[0]) # une liste pour ensuite voir si la piece demandé n'existe pas deja
            if (ide in test):
                return render_template('ajout_piece.html',liste_id=liste_id, err_quant= err_quant, msg="Cette piece existe deja")
            else : #ajouter un createur d'id apres
                cur.execute("INSERT INTO piece('nom', 'quantite', 'id_piece') VALUES (?,?,?)", (nome,quantitee,ide))
                con.commit()
                con.close()
                msg = ''
                return(redirect(url_for('ajout_piece')))
        else :
            return render_template('ajout_piece.html',liste_id=liste_id, err_quant= err_quant, msg="il faut saisir un nom et un id")
    return render_template('ajout_piece.html', liste_id=liste_id, err_quant= err_quant, msg=msg); # LES PROGRAMMEURS a retoucher / separer  fonctions

@app.route('/Agilog/Initialisation/supp', methods=['GET', 'POST'])
def supprimer_piece() :
    if not request.method == 'POST':
        return render_template('ajout_piece.html',liste_id=liste_id, err_quant= "", msg="",testnom="la methode n'est pas post")
    else :
        nomdele=request.form.get('nomdele','')
        con = lite.connect('AgiWeb_BDD.db') #attention chez toi c'est pas rangé au meme endroit
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute ("DELETE FROM 'piece' WHERE nom=?", [nomdele])
        con.commit()
        con.close()
        return(redirect(url_for('ajout_piece')))
    return(redirect(url_for('ajout_piece')))

@app.route('/Agilog/Initialisation/Gestion_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def gestion_stock():
    #var

    msg =""

    #recupere nom des objets pour le vollet deroulant

    con = lite.connect("AgiWeb_BDD.db")
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT nom FROM piece")
    liste_nom = cur.fetchall()

    nome=request.form.get('nome','')
    seuile=request.form.get('seuile','')
    secue=request.form.get('secue','')
    delaie=request.form.get('delaie','')
    #test si ce sont bien des entiers
    if not request.method == 'POST':
        con.close()
        return render_template('gestion_stock.html', liste_nom=liste_nom, msg = "")
    else :
        if (nome!="" and seuile!="" and secue!="" and delaie!=""):
            try:
                seuile=int(seuile)
                secue=int(secue)
                delaie=int(delaie)
                assert seuile >= 0 and secue>=0 and delaie>=0
            except ValueError:
                con.close()
                return render_template('gestion_stock.html', liste_nom=liste_nom, msg = "attention il faut saisir un entier !")
            except AssertionError:
                con.close()
                return render_template('gestion_stock.html', liste_nom=liste_nom, msg = "attention il faut saisir un entier positif !")
            cur.execute("UPDATE Piece SET seuil_recomp=?, stock_secu=?, delai_reappro=? WHERE nom=?", [seuile,secue,delaie,nome])
            con.commit()
            con.close()
            return redirect(url_for('gestion_stock'))
        else:
            con.close()
            return render_template('gestion_stock.html', liste_nom=liste_nom, msg = "attention vous n'avez rien saisi")

    return render_template('gestion_stock.html', liste_nom=liste_nom, msg = "")

@app.route('/Agilog/Initialisation/Code_kit', methods=['GET', 'POST'])
def code_kit():
    #variable
    contenu=""
    c= False
    d= False
    #On crée un kit ou on en choisit un
    kit= recupere_interraction(1,contenu)
    #On choisit un kit existant
    con = lite.connect('AgiWeb_BDD.db')
    con.row_factory = lite.Row
    cur=con.cursor()
    cur.execute("SELECT nom_kit FROM kit;")
    base=cur.fetchall()#variable pour le menu déroulant
    #historique des kit existant
    cur.execute("SELECT id_kit FROM kit;")
    id_kit=cur.fetchall()
    if not request.method == 'POST':
        con.close()
        return render_template('ajout_piece.html',liste_id=liste_id, err_quant= "", msg="")
    else:
        c=compare_nom(request.form.get('nom_kit1'),base)
        d=compare_nom(request.form.get('id_kit'),id_kit)
        dico_kit=[]
        for chose in id_kit :
            cur.execute('SELECT piece, quantite FROM compo_kit WHERE kit=?;',[chose[0]])
            dico_kit.append(cur.fetchall())#historique est une liste de dictionnaire ou chaque dictionnaire est un kit
        if c or d:#le nom du kit est déjà existant, on revient au départ
            con.close()
            return(render_template("Code_kit_init.html", msg ="attention le kit existe deja ",tab_piece=dico_kit,liste_kit=base,liste_id=id_kit))
        else :
            kit_a_modif=request.form.get('nom_kit1')
            con.close()
            return(modif_kit(kit_a_modif))
    return(render_template("Code_kit_init.html", msg ="",tab_piece=dico_kit,liste_kit=base,liste_id=id_kit))

@app.route('/Agilog/Initialisation/Code_kit/modif_kit', methods=['GET', 'POST'])
def modif_kit(kit_a_modif):

    return(render_template('modif_kit_init.html'))

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
