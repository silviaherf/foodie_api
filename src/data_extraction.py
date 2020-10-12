import requests
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


def get_venue_foursquare(food='food',price=[1,2]):
    
    """
    This function makes a request to a URL and returns its response.
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
    This function makes a request to a URL and returns its response.
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
    name=res.json()['response']['groups'][0]['items'][i]['venue']['name']
    address=res.json()['response']['groups'][0]['items'][i]['venue']['location']['formattedAddress'][0]
    lat=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lat']
    long=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lng']
    chincheta = Marker(location=[lat,long], tooltip=name)
    chincheta.add_to(map)


def generate_map(res,place):
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



 #exportar folium a variable apra visualizar en return endpoint
    #with NamedTemporaryFile() as temp:
    #    m.save(f'{temp}.html')

    #return temp.name






