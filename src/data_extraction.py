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


def get_venue_foursquare(food='burger'):
    
    """
    This function makes a request to a URL and returns its response.
    """
    api_user=os.getenv('CLIENT_ID')
    api_key=os.getenv('CLIENT_SECRET')    

    g = geocoder.ip('me')
    lat,long=g.latlng
    location=f'{str(lat)},{str(long)}'
    

    today = date.today().strftime("%Y%m%d")
    
    baseUrl="https://api.foursquare.com"
    endpoint=f'/v2/venues/explore/?ll={location}&query={food}&limit=5&sortByDistance=1&sortByPopularity=1&client_id={api_user}&client_secret={api_key}&v={today}'
 
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url)
        
    data = res.json()
    if res.status_code != 200:
        
        raise ValueError(f'Invalid FourSquare API call: {res.status_code}')
                         #: {data["message"]}\nSee more in {data["documentation_url"]}')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
        
        return res

def generate_map():
    g = geocoder.ip('me')
    lat,long=g.latlng
    location=f'{str(lat)},{str(long)}'
    m = Map(location=g.latlng,zoom_start=15)

  
    m.save('output/mapa.html')


    #with NamedTemporaryFile() as temp:
    #    m.save(f'{temp}.html')

    #return temp.name

