from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Setup flask
app = Flask(__name__)

# Establish mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #Find record of data from mongo db
    mars = mongo.db.mars.find_one()


    #print("m image_urls: ", mars["image_urls"])
    #Return template and data
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    # Run scrape function
    mars_data = scrape_mars.scrape()
    
    # Update mongo database 
    mars.update_many({},{"$set": mars_data}, upsert=True)
    
    #Return to homepage
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()