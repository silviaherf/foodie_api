import os
from dotenv import load_dotenv
load_dotenv()
import requests
from flask import Flask,request, Response, redirect, url_for, render_template, jsonify
import re
import numpy as np
import cv2
import src.data_extraction as extract
import json
from bson.json_util import dumps
import base64
import webbrowser
from geopy.geocoders import Nominatim
import geocoder
import urllib.request
from translate import Translator



app = Flask("foodie")


@app.route("/")

    #This is just the first view of the API
   
def saludo():
    cover = open('src/html/cover.html', 'r', encoding='utf-8').read() 
    return cover


@app.route("/search")

def ask_restaurant():
    search = open('src/html/search.html', 'r', encoding='utf-8').read() 
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

            if res.json()['meta']['code'] != 200:
                return redirect("/search/results/error2")


        elif not food and price:
            res=extract.get_venue_foursquare_near(place=place,price=price)

            if res.json()['meta']['code'] != 200:
                return redirect("/search/results/error2")
       
        locator = Nominatim(user_agent='myGeocoder')
        location=list(locator.geocode(place)[1])

    else:
        if price and food:
            res=extract.get_venue_foursquare(food=food,price=price)

            if res.json()['meta']['code'] != 200:
                return redirect("/search/results/error2")

        elif not food and price:
            res=extract.get_venue_foursquare(price=price)

            if res.json()['meta']['code'] != 200:
                return redirect("/search/results/error2")
 
        g = geocoder.ip('me')
        location=g.latlng


    if res.json()['response']['totalResults']==0:
        return redirect("/search/results/error")

    else:
        extract.generate_map(res=res,place=location)
        
        #map = extract.generate_map(res=res,place=location)._repr_html_()
        return open('src/html/restaurants.html').read()
        #return render_template('restaurants.html',mapa=extract.generate_map(res=res,place=location))
     
        #return map


@app.route("/search/results/mapa")

    #It returns the map in order to set it in the iframe HTML

def show_map():
    map = open('output/mapa.html', 'r', encoding='utf-8').read() 
    return map





@app.route("/search/results/error")

    #It returns a warning in case your query did not find any restaurant

def warning():
    warning = open('src/html/warning.html', 'r', encoding='utf-8').read() 
    return warning

@app.route("/search/results/error2")

    #It returns a warning in case you status code of response is not 200

def warning2():
    warning2 = open('src/html/warning2.html', 'r', encoding='utf-8').read() 
    return warning2


@app.route("/upload")
def upload_image():
    upload = open('src/html/upload_plate.html', 'r', encoding='utf-8').read() 
    return upload

"""
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

"""

@app.route("/calculate",methods=['GET','POST'])
def show_kcals():
    if request.method=='POST':
        image = request.form.get('image')
        url = request.form.get('url')

    if image:

        plate=extract.plate_recognition(image)
    
    elif url:

        urllib.request.urlretrieve(url, 'src/downloads/image.jpg')
        image='src/downloads/image.jpg'
        plate=extract.plate_recognition(image)

     
    translator= Translator(from_lang='es', to_lang="en")
    recipe = translator.translate(plate)


    calories=extract.get_calories(recipe=recipe)


    return render_template('calories.html',plate=recipe.lower(),calories=[calories.to_html(classes='data', header="true")])
   

        
    
"""
@app.route("/calculate/results")
def nutrition_facts():
   
    nutritional=open('src/html/calories.html', 'r', encoding='utf-8').read()

    return nutritional

"""