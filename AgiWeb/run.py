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
    cur.execute("SELECT id FROM production")
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
    a=0
    d=cur.execute(" SELECT datetime('now')")
    if (num_kite!=""):
        d=cur.execute(" SELECT datetime('now')")
        cur.execute("INSERT INTO production('id', 'kit', 'fini','date') VALUES (?,?,?,?)", [newid ,num_kite ,1, d ])
    #con.commit()#enregistrer la requete de modification.
    cur.execute("SELECT id, kit, fini, date FROM Production;")
    liste = cur.fetchall()
    #
    for chaque in liste:
        contenu += "<br/>"
        contenu += str(chaque[0]) + " "
        contenu += str(chaque[1]) + " "
        contenu += str(chaque[2]) + " "
        contenu += str(chaque[3]) + " "
    con.close()

    return contenu;

@app.route('/Agilog/Encours/Aff_stock', methods=['GET']) #la page pour passer une commande
def commande():

    contenu = ""
    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT datetime('now')")
    d=str(cur.fetchall()[0][0])
    contenu += d

    cur.execute("SELECT nom FROM piece")
    nom = cur.fetchall()
    liste_nom=liste(nom)
    cur.execute("SELECT quantite FROM piece")
    quantite = cur.fetchall()
    liste_quantite=liste(quantite)
    cur.execute("SELECT seuil_recomp FROM piece")
    seuil = cur.fetchall()
    liste_seuil=liste(seuil)
    cur.execute("SELECT id FROM piece")
    ide = cur.fetchall()
    liste_id=liste(ide)

    #données du tableau reel
    colonne_reel=["nom", "quantite", "id"]
    reel=tableau("piece",colonne_reel)
    #données du tableau en cours jointure compliqué a finir
    #cur.execute("SELECT compo_commande.commande, compo_commande.piece, compo_commande.quantite, fournisseur.delai

    #(SELECT fournisseur.delai FROM fournsseur JOIN piece ON piece.fournisseur=fournisseur.nom)
    for i in range (0,len(reel)):
        for j in range (0,len(reel[i])):
            contenu += str(reel[i][j])
            contenu += "<br/>"
        contenu += "<br/> <br/>"

    seuil_commande (liste_quantite,liste_seuil,liste_nom)

    # Selection piece AgiGreen à commander
    #cur.execute("SELECT nom FROM piece WHERE a_commander=? and fournisseur=?) VALUE(?,?)",(1,"AgiGreen"))
    #liste_G=cur.fetchall
    #liste_AgiGreen=[]
    #liste_AgiGreen[0]=liste(liste_G[0])
    #liste_AgiGreen[1]=liste(liste_G[1])

    # Selection piece AgiPart à commander


    # c'est pour voir si ca marche c'est tout
    cur.execute("SELECT a_commander FROM piece")
    commande = cur.fetchall()
    liste_commande=liste(commande)
    for i in range (0,len(liste_commande)):
        print (liste_commande[i])
        print (liste_nom[i])

    con.commit
    con.close

    return contenu
#La page Initialisation
@app.route('/Agilog/Initialisation')
def initialisation ():
    return render_template('initialisation_alog.html')

@app.route('/Agilog/Initialisation/Ajout_piece', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def ajout_piece():
    # la demande du nom de la piece à rajouter et du stock à mettre
    contenu=""
    contenu += "<form method='get' action='Ajout_piece'>"
    contenu += "nom de la piece <br/>"
    contenu += "<input type='text' name='nom' value=''>"
    contenu += "<br/>"
    contenu += "stock de depart <br/>"
    contenu += "<input type='int' name='quantite' value=''>"
    contenu += "<br/>"
    contenu += "ton id <br/>"
    contenu += "<input type='text' name='id' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    # On ajoute la pièce à la base de donnée
    nome=request.args.get('nom','')
    quantitee=request.args.get('quantite','')
    ide=request.args.get('id','')
    base="piece"
    colonne=["nom", "id", "quantite"]
    entree=[nome, ide, quantitee]
    types=[str, str, int]
    if (testin(base,"nom", nome)==1 or testin(base, "id", ide)==1): # test pour voir si le nom ou l'id existe deja
        contenu += "<br/> cette piece existe deja <br/>"
    else:
        ajout_bdd(base, colonne, entree, types)

    contenu += "<form method='get' action='gestion_stock'>"
    contenu += "<br/><br/> quel est le nom de la piece que tu veux tu supprimer? <br/>"
    contenu += "<input type='str' name='nomdel' value=''>"
    contenu += "<input type='submit' value='Envoyer'>"

    # on supprime une piece de la bdd
    nomdele=request.args.get('nomdel','')
    delete('piece', 'nom', nomdele)

    # un affichage des stocks rapide pour tester
    con = lite.connect(cheminbdd) #attention chez toi c'est pas rangé au meme endroit
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT nom, quantite, id FROM Piece;")
    liste = cur.fetchall()
    #
    for chaque in liste:
        contenu += "<br/>"
        contenu += str(chaque[0]) + " "
        contenu += str(chaque[1]) + " "
        contenu += str(chaque[2]) + " "

    con.commit()
    con.close()

    return contenu; # LES PROGRAMMEURS a retoucher / separer  fonctions

@app.route('/Agilog/Initialisation/Gestion_stock', methods=['GET', 'POST'])#recupere 2 variable nom et prnom et les ajoutent a la base de données (a modifier pour mettre piece et quantite)
def gestion_stock():
    contenu=""

    #demande le nom de la piece, le seuil de recompletement, le stock de secu et le delai de reapro a changer en fournisseur
    contenu += "<form method='get' action='Gestion_stock'>"
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
    secue=request.args.get('secu','')
    delaie=request.args.get('delai','')
    #test si ce sont bien des entiers

    base="Piece"
    colonne=["seuil_recomp", "stock_secu", "delai_reappro", "nom"]
    entree=[seuile,secue,delaie,nome]
    types=[int, int, int, str]
    if (testin(base,"nom", nome)==0 and test_rien(entree)==0): # test pour voir si le nom existe
        contenu += "<br/> cette piece n'existe pas <br/>"
    else:
        mise_a_jour_bdd(base, colonne, entree, types)

    # ceci est juste un affichage basique de la bdd, a remplacer par un vrai tableau
    con = lite.connect(cheminbdd)
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT nom, quantite, id, seuil_recomp, stock_secu, delai_reappro FROM Piece;")
    liste = cur.fetchall()
    for chaque in liste:
        contenu += "<br/>"
        contenu += str(chaque[0]) + " "
        contenu += str(chaque[1]) + " "
        contenu += str(chaque[2]) + " "
        contenu += str(chaque[3]) + " "
        contenu += str(chaque[4]) + " "
        contenu += str(chaque[5])
    con.close()
    #contenu += render_template('affichage_personnes.html', personnes = lignes)#une fonction html pour afficher un tableau

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
