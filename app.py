import os,json
from flask import Flask , render_template , request
import requests

#load the Azure maps key from the .env file 
MAP_KEY= os.environ["MAP_KEY"]
WAQI_API_KEY= os.environ["WAQI_API_KEY"]
WAQI_API_URL = "https://api.waqi.info/map/bounds/?latlng={},{},{},{}&token={}"

#initialize the Flask app
app = Flask(__name__)
#handle requests to the root of the website and returning the home page
@app.route("/")
def home():
    # Data for the home page to pass the maps key
    data={"map_key": MAP_KEY }
    #returning the rendered html page
    return render_template("home.html",data=data)


#Load air quality data 

def get_color(aqi):
    if aqi<=50 :
        return "#009966" #dark green
    if aqi <= 100 :
        return "#ffde33" #yellow
    if aqi <= 150 :
        return "#ff9933" #orange
    if aqi <= 200 :
        return "#cc0033" #red
    if aqi <= 300 :
        return "#660099" #purple
    return "#7e0023" #brown

def load_aqi_data(point1,point2,point3,point4):

    #load air quality data
   url= WAQI_API_URL.format(point1,point2,point3,point4,WAQI_API_KEY)
   aqi_data=requests.get(url)


   #creating a geoJSON feature collection from the obtained data
   feature_collection={
       "type" : "FeatureCollection",
       "features" : []
   }

   for value in aqi_data.json()["data"]:
       if value['aqi'] != '-':
           feature_collection["features"].append({
               "type" : "Feature",
               "geometry" : {
                   "type" : "Point",
                   "coordintates" : [value['lon'], value["lat"]]
                   
               },

               "properties" : {
                   "color" : get_color(int(value["aqi"]))
               }

           })
    
   return feature_collection


@app.route("/aqi", methods=["GET"])
def aqi_data():
    #getting bounds from the request
    bound=request.args["bounds"].split(",")
    #loading the aqi data and converting it in geoJSON for the given bounds
    return json.dumps(load_aqi_data(bound[0],bound[1],bound[2],bound[3]))



