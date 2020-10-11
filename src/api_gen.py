import os
from dotenv import load_dotenv
load_dotenv()
import requests
from flask import Flask,request, Response, redirect, url_for
import re
import src.data_extraction as extract
import json
from bson.json_util import dumps
import base64
import branca
import webbrowser
from geopy.geocoders import Nominatim
import geocoder



app = Flask("foodie")

@app.route("/")

    #This is just the first view of the API
   
def saludo():
    cover = open('src/cover.html', 'r', encoding='utf-8').read() 
    return cover


@app.route("/search")

def ask_restaurant():
    search = open('src/search.html', 'r', encoding='utf-8').read() 
    return search




@app.route("/search/results",methods=['GET', 'POST'])

    #Using a POST method, you can tell the API what you want to eat in a restaurant nearby
    #place just in case IP location doesn't work on the cloud

def return_restaurants():
    prices={'€':1,'€€':2,'€€€':3,'€€€€':4}
    
    if request.method=='POST':
        place = request.form.get('place')
        food = request.form.get('food')
        price_post = request.form.get('price')
        if price_post:
            price=prices[price_post]
        else:
            price=2


    elif request.method=='GET':
        place = request.args.get("place")
        food = request.args.get('food')
        price = request.args.get('price')
  
       
    if place:
        if price and food:
            res=extract.get_venue_foursquare_near(place=place,food=food,price=price)


        elif not food and price:
            res=extract.get_venue_foursquare_near(place=place,price=price)

       
        locator = Nominatim(user_agent='myGeocoder')
        location=list(locator.geocode(place)[1])

    else:
        if price and food:
            res=extract.get_venue_foursquare(food=food,price=price)

        elif not food and price:
            res=extract.get_venue_foursquare(price=price)
 
        g = geocoder.ip('me')
        location=g.latlng

    if res.json()['response']['totalResults']==0:
        return redirect("/search/results/error")

    else:
        extract.generate_map(res=res,place=location)
        resultados = open('src/restaurants.html', 'r', encoding='utf-8').read() 
        
        #map = open(extract.generate_map(), 'r', encoding='utf-8').read() 
        return resultados


@app.route("/search/results/error")

    #Using a POST method, you can tell the API what you want to eat in a restaurant nearby
    #place just in case IP location doesn't work on the cloud

def warning():
    warning = open('src/warning.html', 'r', encoding='utf-8').read() 
    return warning



@app.route("/calculate",methods=['POST'])
def calculate_kcals():
    
    pass


