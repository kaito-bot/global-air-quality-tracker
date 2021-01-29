import os,json
from flask import Flask , render_template , request
import requests

#load the Azure maps key from the .env file 
MAP_KEY= os.environ["MAP_KEY"]

#initialize the Flask app
app = Flask(__name__)
#handle requests to the root of the website and returning the home page
@app.route("/")
def home():
    # Data for the home page to pass the maps key
    data={"map_key":MAP_KEY}
    #returning the rendered html page
    return render_template("home.html",data=data)


