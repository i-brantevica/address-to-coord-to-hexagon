from geopy.geocoders import GoogleV3, Nominatim
from datetime import date
import pandas as pd
import os
import h3

dir = os.getcwd()
file = dir + '/example_data.csv'
coord_file = dir + '/example_data-coord-hex.csv'

df = pd.read_csv(file,encoding='utf-8', sep = ";")

df['full_address'] = df['address'] + ', Riga, Latvia'

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="extract_coord_and_hex")

# Define a function to get coordinates from an address
def get_coordinates(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return get_coordinates(address)  # Retry if timeout occurs

# Apply the function to your DataFrame
lat, lon = zip(*df['full_address'].apply(get_coordinates))

df['lat'] = lat
df['lon'] = lon

# Print the updated DataFrame
print(df)

# Define the H3 resolution level
resolution = 8  # Adjust the resolution level as needed

# Define a function to get H3 hexagon for a given latitude and longitude
def get_h3_hexagon(row):
    h3_index = h3.geo_to_h3(row['lat'], row['lon'], resolution)
    return h3_index

# Apply the function to your DataFrame
column = 'h3_hexagon_res' + str(resolution)
df[column] = df.apply(get_h3_hexagon, axis=1)

# Print the updated DataFrame
print(df)

df.to_csv(coord_file,index=False,encoding='utf-8', sep = ";")

