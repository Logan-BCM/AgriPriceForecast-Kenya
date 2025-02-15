import pandas as pd
import time
from geopy.geocoders import Nominatim

# Specify the column name that contains the market names
location_column = 'Market'  # Adjust if your column name is different

# Initialize the geocoder with a custom user agent
geolocator = Nominatim(user_agent="geo_coordinates_app")

def get_coordinates(place):
    """
    Geocode a place in Kenya and return the latitude and longitude.
    If the location is not found, return (None, None).
    """
    try:
        location = geolocator.geocode(f"{place}, Kenya")  # Ensuring all searches are within Kenya
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding '{place}': {e}")
        return None, None

# Dictionary to cache geocoding results for markets
cache = {}

# Lists to store the latitude and longitude for each market
latitudes = []
longitudes = []

def geolocate_markets(combined_df):
    """Add latitude and longitude columns to the DataFrame."""
    total = len(combined_df[location_column])
    
    for idx, place in enumerate(combined_df[location_column], start=1):
        print(f"Processing {idx}/{total}: {place}")
        
        # Check if this market's coordinates have already been retrieved
        if place in cache:
            lat, lon = cache[place]
        else:
            lat, lon = get_coordinates(place)
            cache[place] = (lat, lon)
            time.sleep(1)  # Pause to respect geocoder limits
        
        latitudes.append(lat)
        longitudes.append(lon)
    
    # Add the 'latitude' and 'longitude' columns to the DataFrame
    combined_df['latitude'] = latitudes
    combined_df['longitude'] = longitudes
    
    # Save the updated DataFrame to a new CSV file
    combined_df.to_csv("combined_with_coordinates.csv", index=False)
    print("Coordinates have been added and saved to 'combined_with_coordinates.csv'.")
