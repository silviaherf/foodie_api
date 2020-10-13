import os
from dotenv import load_dotenv
load_dotenv()
import requests
from flask import Flask,request, Response, redirect, url_for, render_template
import re
import src.data_extraction as extract
import json
from bson.json_util import dumps
import base64
import webbrowser
from geopy.geocoders import Nominatim
import geocoder
import urllib.request



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
        #map = open('output/mapa.html', 'r', encoding='utf-8').read() 
        
        
        map = extract.generate_map(res=res,place=location)._repr_html_()
        #return open('src/html/restaurants.html').read().format(mapa=map)
     
        return map


@app.route("/search/results/error")

    #It returns a warning in case your query did not find any restaurant

def warning():
    warning = open('src/html/warning.html', 'r', encoding='utf-8').read() 
    return warning



@app.route("/upload")
def upload_image():
    upload = open('src/html/upload_plate.html', 'r', encoding='utf-8').read() 
    return upload



@app.route("/calculate",methods=['POST'])
def show_kcals():
    image = request.form.get('image')
    url = request.form.get('url')

    if image:

        plate=extract.class_recognition(image)
    
    elif url:

        urllib.request.urlretrieve(url, 'src/downloads/image.jpg')
        image='src/downloads/image.jpg'
        plate=extract.class_recognition(image)

    
    calories=extract.get_calories(recipe=plate)

    #calculator= open('src/html/calories.html', 'r', encoding='utf-8').read().format(p=calories,c=calories) 

    

    return open('src/html/calories.html', 'r', encoding='utf-8').read().format(plate=plate, calories=calories)


