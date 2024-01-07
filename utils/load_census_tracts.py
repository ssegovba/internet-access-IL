import sys
import os

sys.path.append(os.path.abspath(".."))

import pandas as pd
import geopandas as gpd
import json
import geojson

DATA_PATH = "../data/"


def create_census_json():
    boundaries = gpd.read_file(DATA_PATH + "tl_2020_17_tract20/tl_2020_17_tract20.shp")

    # Convert Shapefile to GeoJSON
    tracts_json = boundaries.to_json()
    tracts_json = json.loads(tracts_json)

    # Save the data to a JSON file
    with open(DATA_PATH + "tracts.json", "w") as file:
        json.dump(tracts_json, file)


# ----------------------------------------

# Calling the function to create json file

create_census_json()
