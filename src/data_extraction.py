import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import date
import geocoder
from folium import Map, Marker, Icon, FeatureGroup, LayerControl
from folium.plugins import HeatMap
import webbrowser
import glob
import cv2
from geopy.geocoders import Nominatim
import tensorflow as tf
from translate import Translator


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
    'radius':500,
    'query':food,
    'limit':5,
    'sortByDistance':1,
    'price':price,
    'client_id':api_user,
    'client_secret':api_key,
    'v':today
    }

    
    
    baseUrl="https://api.foursquare.com"
    endpoint='/v2/venues/explore/'
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url,params=params)
        
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
    'radius':500,
    'query':food,
    'limit':5,
    'sortByDistance':1,
    'price':price,
    'client_id':api_user,
    'client_secret':api_key,
    'v':today
    }

    
    baseUrl="https://api.foursquare.com"
    endpoint='/v2/venues/explore/'
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url,params=params)
        
    if res.json()['meta']['code'] != 200:
        
        print('¿Seguro que has escrito bien tu ubicación y lo que te apetece comer?')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
        
    return res


def make_markers(res,map,i=0):
    """
    This function makes a request to Spooncaular API for a recipe and returns its response.
    """
    name=res.json()['response']['groups'][0]['items'][i]['venue']['name']
    address=res.json()['response']['groups'][0]['items'][i]['venue']['location']['formattedAddress'][0]
    tipo=res.json()['response']['groups'][0]['items'][i]['venue']['categories'][0]['name']
    translator= Translator(from_lang='en', to_lang="es")
    tipo= translator.translate(tipo)
    lat=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lat']
    long=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lng']
    chincheta = Marker(location=[lat,long], tooltip=name, popup=address, icon=Icon(color='blue',icon='cutlery', prefix='glyphicon'))
    chincheta.add_to(map)


def generate_map(res,place):
    """
    This function creates a Folium map with the results from FourSquare API
    """
    m = Map(location=place,zoom_start=15)
    if res.json()['response']['totalResults']>0 and res.json()['response']['totalResults']<5:
        for i in range(0,res.json()['response']['totalResults']):
            make_markers(res=res,map=m,i=i)
        m.save('output/mapa.html')
    elif res.json()['response']['totalResults']>=5:
        for i in range(0,5):
            make_markers(res=res,map=m,i=i)
        m.save('./output/mapa.html')
    return m


def plate_recognition(image):
    """
    This function uses NN for image recognition
    """
    clases={'hamburguesa': 0, 
    'pizza': 1, 
    'espagheti boloñesa': 2, 
    'sushi': 3, 
    'tacos': 4}
    model = tf.keras.models.load_model('output/models/14_oct/InceptionV5_model.hdf5')
    img = cv2.imread(image)
    img2 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img2=img2/255
    dim=(256,256)
    image=cv2.resize(img2, dim,interpolation=cv2.INTER_AREA)
    image = np.expand_dims(image, axis=0) 
    pred = model.predict(image)
    for k,v in clases.items():
        if v==np.argmax(pred,axis=1):
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
        
    if res.status_code != 200:
        
        raise ValueError(f'Invalid Spoonacular API call: {res.status_code}')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
    
        try:
            res.json()['status']=='error'
            print('No hay datos suficientes para esta búsqueda; por favor, prueba con algo menos específico')

        except: 
            df=create_calories_df(res=res,recipe=recipe)

            return df
                  
        
def allowed_file(filename):
    
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions 


def create_calories_df(res,recipe):
    cal=res.json()['calories']['value']
    fat=res.json()['fat']['value']
    protein=res.json()['protein']['value']
    carbs=res.json()['carbs']['value']

    nutrition={ 'Calorias':f'{cal} kcal',
            'Grasa':f'{fat} g',
            'Proteina':f'{protein} g',
            'Carbohidratos':f'{carbs} g'
        
    }

    df=pd.DataFrame.from_dict(nutrition,orient='index',columns=['Valores nutricionales por 100g'])

    return df


    

