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


def get_venue_foursquare(food='burger',price=2):
    
    """
    This function makes a request to a URL and returns its response.
    """
    api_user=os.getenv('CLIENT_ID')
    api_key=os.getenv('CLIENT_SECRET')    

    g = geocoder.ip('me')
    lat,long=g.latlng
    location=f'{str(lat)},{str(long)}'
    today = date.today().strftime("%Y%m%d")

    params={'ll':location,
    'query':food,
    'limit':5,
    'll':location,
    'sortByDistance':1,
    'sortByPopularity':0,
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

def get_venue_foursquare_near(place,food='burger',price=2):
    
    """
    This function makes a request to a URL and returns its response.
    """
    api_user=os.getenv('CLIENT_ID')
    api_key=os.getenv('CLIENT_SECRET')    


    today = date.today().strftime("%Y%m%d")

    params={'near':place,
    'query':food,
    'limit':5,
    'll':location,
    'sortByDistance':1,
    'sortByPopularity':0,
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




def generate_map(res):
    g = geocoder.ip('me')
    lat_me,long_me=g.latlng
    location=f'{str(lat_me)},{str(long_me)}'
    m = Map(location=g.latlng,zoom_start=15)

    

    for i in range(0,5):
        name=res.json()['response']['groups'][0]['items'][i]['venue']['name']
        address=res.json()['response']['groups'][0]['items'][i]['venue']['location']['address']
        lat=res.json()['response']['groups'][0]['items'][i]['venue']['location']['labeledLatLngs'][0]['lat']
        long=res.json()['response']['groups'][0]['items'][1]['venue']['location']['labeledLatLngs'][0]['lng']
        chincheta = Marker(location=[lat,long], tooltip=name)
        chincheta.add_to(m)

  
    m.save('output/mapa.html')



 #exportar folium a variable apra visualizar en return endpoint
    #with NamedTemporaryFile() as temp:
    #    m.save(f'{temp}.html')

    #return temp.name





def pictures_to_df(path="../input/images/"):

    dishes = [*glob.glob(f"{path}/**/*.jpg"), *glob.glob(f"{path}/**/*.JPG")]
    pictures = pd.DataFrame({
        "path": dishes
    })

    pictures['dish']=df.path.apply(lambda x: x.split("/")[3])
    return pictures


