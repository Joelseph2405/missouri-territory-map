from geocoder import geocode_address

address = "5251 Highway 47"
city = "Washington"
zip_code = "63090"

print(f"Geocoding: {address}, {city} {zip_code}")
lat, lng = geocode_address(address, city, zip_code)
print(f"Result: {lat}, {lng}")

# Try variation
address_var = "5251 MO-47"
print(f"Geocoding Variation: {address_var}, {city} {zip_code}")
lat2, lng2 = geocode_address(address_var, city, zip_code)
print(f"Result Variation: {lat2}, {lng2}")
