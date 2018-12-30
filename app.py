from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

#setup mongo db
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

#drop any pre-existing collection
db.mars.drop()

variable = scrape()



@app.route("/")
def index():
	print(variable)
	return render_template("index.html", variable = variable)


@app.route("/scrape")
def scraper():
	variable = scrape()
	return redirect("/", code=302)

	
if __name__ == "__main__":
    app.run(debug=True)