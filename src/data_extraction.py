import requests
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import date


def get_venue_foursquare(place='Madrid',food='burger'):
    
    """
    This function makes a request to a URL and returns its response.
    """
    api_user=os.getenv('CLIENT_ID')
    api_key=os.getenv('CLIENT_SECRET')    
    

    today = date.today().strftime("%Y%m%d")
    
    baseUrl="https://api.foursquare.com"
    endpoint=f'/v2/venues/explore/?near={place}&query={food}&limit=5&sortByDistance=1&sortByPopularity=1&client_id={api_user}&client_secret={api_key}&v={today}'
 
    url = f"{baseUrl}{endpoint}"
    

    res = requests.get(url)
        
    data = res.json()
    if res.status_code != 200:
        
        raise ValueError(f'Invalid FourSquare API call: {res.status_code}')
                         #: {data["message"]}\nSee more in {data["documentation_url"]}')
        
    else:
        print(f"Requested data to {baseUrl}; status_code:{res.status_code}")
        
        return res