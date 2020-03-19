from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
	return "<h1>HELLO WORLD</h1>"


@app.route("/edwin")
def blah():
	return "<h1>blah</h1>"
