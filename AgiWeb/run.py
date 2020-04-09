from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("accueil.html", prenom = "Bat")

@app.route("/AgiLean_accueil")
def leanacc():
	return render_template("AgiLean_accueil.html")

@app.route("/AgiLog_accueil")
def logacc():
	return render_template("AgiLog_accueil.html")

@app.route("/initialisation")
def initialisation():
	conn = sqlite3.connect("AgiWeb_BDD.db")
	cursor = conn.cursor()
	cursor.execute("select id_piece from piece")
	list_id = cursor.fetchall()
	conn.close()
	return render_template("initialisation.html", list_id_piece=list_id)
