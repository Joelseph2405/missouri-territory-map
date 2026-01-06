import requests
import time
from urllib.parse import quote

# Agent string to identify our application to Nominatim
USER_AGENT = "BlackBoxCRM/1.0 (internal-tool)"

def geocode_address(address, city, zip_code):
    """
    Geocode an address using OpenStreetMap Nominatim API.
    Returns (lat, lng) or None if not found.
    Respects the 1-second rate limit.
    """
    
    # Construct query
    query = f"{address}, {city}, MO {zip_code}"
    encoded_query = quote(query)
    
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
    
    try:
        headers = {
            'User-Agent': USER_AGENT
        }
        
        # Be nice to the API
        time.sleep(1.1) 
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None, None
            
    except Exception as e:
        print(f"Geocoding error for {query}: {e}")
        return None, None
