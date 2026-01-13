from geocoder import geocode_address

lat, lng = geocode_address("301 Wilmer Valley Drive", "Wentzville", "63385")
print(f"HOME_COORDS: {lat}, {lng}")
