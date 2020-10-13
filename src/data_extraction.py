import requests
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import date
import geocoder
from folium import Map, Marker, Icon, FeatureGroup, LayerControl, Choropleth
import branca
from folium.plugins import HeatMap
from tempfile import NamedTemporaryFile
import webbrowser
import glob
import cv2
from geopy.geocoders import Nominatim
import cgi, cgitb
import tensorflow as tf


def get_venue_foursquare(food='food',price=[1,2]):
    
    """
    This function makes a request FourSquare API returns its response based on IP adress location.
    """
    api_user=os.getenv('CLIENT_ID')
    api_key=os.getenv('CLIENT_SECRET')    
    today = date.today().strftime("%Y%m%d")


    g = geocoder.ip('me')
    lat,long=g.latlng
    location=f'{str(lat)},{str(long)}'
    
    
    params={'ll':location,
    'radious':2,
    'query':food,
    'limit':5,
    'sortByDistance':1,
    'sortByPopularity':1,
    'price':price,
    'client_id':api_user,
    'client_secret':api_key,
    'v':today
    }

    
    
    baseUrl="https://api.foursquare.com"
    endpoint='/v2/venues/explore/'
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url,params=params)
        
    data = res.json()
    if res.status_code != 200:
        
        raise ValueError(f'Invalid FourSquare API call: {res.status_code}')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
        
        return res


def get_venue_foursquare_near(place,food='food',price=[1,2]):
    
    """
    This function makes a request to FourSquare API taking into account a place and returns its response.
    """
    api_user=os.getenv('CLIENT_ID')
    api_key=os.getenv('CLIENT_SECRET')    
    today = date.today().strftime("%Y%m%d")

  
    params={
    'near':place,
    'radious':2,
    'query':food,
    'limit':5,
    'sortByDistance':1,
    'sortByPopularity':1,
    'price':price,
    'client_id':api_user,
    'client_secret':api_key,
    'v':today
    }

    
    baseUrl="https://api.foursquare.com"
    endpoint='/v2/venues/explore/'
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url,params=params)
        
    data = res.json()
    if res.status_code != 200:
        
        raise ValueError(f'Invalid FourSquare API call: {res.status_code}')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
        
        return res

def make_markers(res,map,i=0):
    """
    This function makes a request to Spooncaular API for a recipe and returns its response.
    """
    name=res.json()['response']['groups'][0]['items'][i]['venue']['name']
    address=res.json()['response']['groups'][0]['items'][i]['venue']['location']['formattedAddress'][0]
    lat=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lat']
    long=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lng']
    chincheta = Marker(location=[lat,long], tooltip=name)
    chincheta.add_to(map)


def generate_map(res,place):
    """
    This function creates a Folium map with the results from FourSquare API
    """
    m = Map(location=place,zoom_start=15)
    if res.json()['response']['totalResults']>0 and res.json()['response']['totalResults']<5:
        for i in range(0,res.json()['response']['totalResults']):
            make_markers(res=res,map=m,i=i)
        #m.save('output/mapa.html')
    elif res.json()['response']['totalResults']>=5:
        for i in range(0,5):
            make_markers(res=res,map=m,i=i)
        #m.save('output/mapa.html')
    return m



def class_recognition(image):
    """
    This function uses NN for image recognition
    """
  
    img = cv2.imread(image)
    img2 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    dim=(75,75)
    image=cv2.resize(img2, dim,interpolation=cv2.INTER_AREA)
    image = np.expand_dims(image, axis=0) 

    model = tf.keras.models.load_model('output/models/full_V3_check.hdf5')
    pred = model.predict(image)
    
    for k,v in test_generator.class_indices.items():
        if v==int(np.where(pred == 1)[1]):
            plate=k
    return plate



def get_calories(recipe='pizza'):
    """
    This function makes a request to Spooncaular API for a recipe and returns its response.
    """
    

    api_key=os.getenv('SPOON_KEY')    

    recipe=recipe.replace(' ','+')

    params={'apiKey':api_key,
    'title':recipe,
   
    }

    
    
    baseUrl=f'https://api.spoonacular.com/'
    endpoint='recipes/guessNutrition'
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url,params=params)
        
    data = res.json()
    if res.status_code != 200:
        
        raise ValueError(f'Invalid Spoonacular API call: {res.status_code}')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
    
        try:
            res.json()['status']=='error'
            print('No hay datos suficientes para esta búsqueda; por favor, prueba con algo menos específico')

        except: 
            pass
                  
        return res





