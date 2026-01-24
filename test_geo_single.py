from geocoder import geocode_address

address = "5251 Highway 47"
city = "Washington"
zip_code = "63090"

print(f"Testing geocode for: {address}, {city}, {zip_code}")
lat, lng = geocode_address(address, city, zip_code)
print(f"Result: {lat}, {lng}")
