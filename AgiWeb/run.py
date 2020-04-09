from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("accueil.html", prenom = "Bat")

@app.route("/AgiLean_accueil")
def leanacc():
	return render_template("AgiLean_accueil.html")
