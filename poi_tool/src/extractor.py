import osmnx as ox
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def geocode_address(address):
    """
    Geocodes an address to latitude and longitude.
    """
    try:
        geolocator = Nominatim(user_agent="poi_tool")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding address: {e}")
        return None, None

def get_pois(latitude, longitude, distance_km=0.5):
    """
    Fetches POIs within a square bounding box centered on the given coordinates.
    """
    north = geodesic(kilometers=distance_km).destination((latitude, longitude), 0).latitude
    south = geodesic(kilometers=distance_km).destination((latitude, longitude), 180).latitude
    east = geodesic(kilometers=distance_km).destination((latitude, longitude), 90).longitude
    west = geodesic(kilometers=distance_km).destination((latitude, longitude), 270).longitude

    bbox = (west, south, east, north)
    tags = {"amenity": True, "shop": True, "leisure": True, "tourism": True, "historic": True}
    
    try:
        pois = ox.features_from_bbox(bbox=bbox, tags=tags)
        
        if pois.empty:
            return pd.DataFrame()

        results = []
        for _, poi in pois.iterrows():
            poi_lat = poi.geometry.centroid.y
            poi_lon = poi.geometry.centroid.x
            
            name = poi.get('name', 'N/A')
            
            category = 'N/A'
            for cat in tags.keys():
                if pd.notna(poi.get(cat)):
                    category = cat
                    break
            
            dist = geodesic((latitude, longitude), (poi_lat, poi_lon)).km
            
            results.append({
                "name": name,
                "category": category,
                "latitude": poi_lat,
                "longitude": poi_lon,
                "distance_from_center_km": dist
            })
            
        return pd.DataFrame(results)

    except Exception as e:
        print(f"An error occurred while fetching POIs: {e}")
        return pd.DataFrame()
