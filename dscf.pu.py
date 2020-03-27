from flask import Flask
app = Flask(__name__)

@app.route("/ed")
def hello_world():
	return "<h1>blahblah</h1>"