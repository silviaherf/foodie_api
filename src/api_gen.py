import os
from dotenv import load_dotenv
load_dotenv()
import requests
from flask import Flask,request, Response
import re
import src.data_extraction as extract
import json
from bson.json_util import dumps
import base64
import branca
import webbrowser




app = Flask("foodie")

@app.route("/")

    #This is just the first view of the API
   
def saludo():
    cover = open('src/cover.html', 'r', encoding='utf-8').read() 
    return cover


@app.route("/search",methods=['GET', 'POST'])

    #Using a POST method, you can tell the API what you want to eat in a restaurant nearby
    #place just in case IP location doesn't work on the cloud

def find_restaurant():
    if request.method=='POST':
        place = request.form.get('place')
        food = request.form.get('food')

    else:
        place=request.args.get("place")
        food = request.args.get('food')
        
    if place:
        res=extract.get_venue_foursquare_near(place,food)
    else:
        res=extract.get_venue_foursquare(food)

    extract.generate_map(res)
    map = open('output/mapa.html', 'r', encoding='utf-8').read() 
    
    #map = open(extract.generate_map(), 'r', encoding='utf-8').read() 
    return map



@app.route("/calculate",methods=['POST'])
def calculate_kcals():
    
    pass


