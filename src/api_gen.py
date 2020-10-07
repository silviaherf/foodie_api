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


app = Flask("foodie")

@app.route("/")

    #This is just the first view of the API
   
def saludo():
    HtmlFile = open('src/cover.html', 'r', encoding='utf-8')
    cover = HtmlFile.read() 
    return cover


@app.route("/search",methods=['POST'])

    #Using a POST method, you can tell the API what you want to eat in a restaurant nearby

def find_restaurant():
    place = request.form.get('place')
    food = request.form.get('food')
    res=extract.get_venue_foursquare(place,food)
    data=res.json()
    restaurants=[]
    for i in range(0,5):
        restaurants.append(data['response']['groups'][0]['items'][i]['venue']['name'])

    return dumps(restaurants)



