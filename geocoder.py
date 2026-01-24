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
    
    # Retry configuration
    max_retries = 3
    base_delay = 1.5

    for attempt in range(max_retries):
        try:
            # Construct query check for empty parts
            parts = [city, "MO", zip_code]
            if address:
                parts.insert(0, address)
            query = ", ".join(parts)
            encoded_query = quote(query)
            
            url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
            
            headers = {
                'User-Agent': USER_AGENT
            }
            
            # Rate limiting with backoff
            sleep_time = base_delay * (attempt + 1)
            time.sleep(sleep_time)
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                print(f"✅ Found data on attempt {attempt+1}")
                return float(data[0]['lat']), float(data[0]['lon'])
            
            # If we get here with no data, maybe return None immediately or continue? 
            print(f"⚠️ No data found for query: {query} (Attempt {attempt+1})")
            return None, None
            
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}/{max_retries} failed for {query}: {e}")
            if attempt == max_retries - 1:
                return None, None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, None
    
    return None, None
