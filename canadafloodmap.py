# Import folium and pandas library
import folium
import pandas
import json

__author__ = "Pathum Danthanarayana"
__version__ = 1.0
__date__ = "June 29, 2022"

# History log
# June 29, 2022 - Version 1.0 created
import pylab as pl

"""
The generate_color function returns a colour based on the 
flood's damage coefficient. If the coefficient is between 
0 and 49, the flood's marker colour will be green (low damage).
If it is between 50 and 99, the flood's marker colour will be orange 
(moderate damage).
Lastly, if it is between 1000 and 1000, the flood's marker colour will be 
red (critical damage).
"""


def generate_color(damage_str: str) -> str:

    # Handle unknown case
    if damage_str == '-':
        return 'blue'
    # Type case str to int
    damage_int = float(damage_str)
    if 0 <= damage_int < 50:
        return 'green'
    elif 50 <= damage_int < 100:
        return 'orange'
    elif 100 <= damage_int <= 1000:
        return 'red'


# Create dataframe object
data = pandas.read_csv("canada_floods.csv")
# Create 5 lists: 1 for latitude, longitude, general location,flood year, and damage columns
latitude = list(data["LATITUDE"])
longitude = list(data["LONGITUDE"])
general_location = list(data["GEN_LOCATION"])
flood_year = list(data["YEAR"])
flood_damage = list(data["DAMAGE"])

# Create a feature group to add the flood location markers to the map
flood_locations_fg = folium.FeatureGroup(name = "Flood Locations")

# Traverse through latitude, longitude, general location, and flood year lists simultaneously
# (e.g. will access element i in each of the 4 lists)
for lat, long, location, year, damage in zip(latitude, longitude, general_location, flood_year, flood_damage):
    # Create a tuple containing the flood's coordinate
    marker_location = (lat, long)
    # Create a string for the marker's popup
    popup_message = "This flood occurred in {0} during {1}.".format(location, year)
    # Add the circle marker to the feature group
    flood_locations_fg.add_child(folium.CircleMarker(location = marker_location, radius = 6, popup = popup_message,
    fill = True, fill_color = generate_color(damage), color = 'white', fill_opacity = 0.9))

# Create list containing map's start location coordinates
start_location = [45.45, -75.59]
# Create the map object
flood_map = folium.Map(start_location, zoom_start = 6, tiles = "Stamen Terrain")

# Create a feature group for the population layer
population_fg = folium.FeatureGroup(name = "Population Density")
# Create and load GeoJSON layer
geojson_layer = folium.GeoJson(json.load(open('world-population.geo.json')), name='geojson',
style_function = lambda x: {'fillColor': 'green' if int(x['properties']['POP2005']) < 10000000 else 'orange' if 10000000 <= int(x['properties']['POP2005']) < 20000000 else 'red'})
# Add GeoJSON layer over basemap with style function
population_fg.add_child(geojson_layer)

# Add the feature groups to the map
flood_map.add_child(population_fg)
flood_map.add_child(flood_locations_fg)

# Add layer control to map
flood_map.add_child(folium.LayerControl())

# Save map
flood_map.save("CanadaFloodMap.html")