import googlemaps
import pandas as pd
import json
from datetime import datetime
from constants import GEOCODING_API_KEY

# Define initial arguments
LIB_CODES = {
    "All": "all",
    "123": "academic",
    "124": "public",
    "125": "school",
    "126": "special",
    "963": "state_lib",
    "964": "regional_system",
    "965": "catalog_consortium",
}


def load_data(lib_type):
    """
    Load the dataset with libraries names and addresses

    Input:
        lib_type (str): a str containing the code of the type of library

    Output:
        data (dict): dictionary with names as keys and addresses as values
    """
    file_name = "../data/clean_lib_data_" + LIB_CODES[lib_type] + ".json"
    with open(file_name) as file:
        data = json.load(file)

    return data


def geocode_lib(lib_dict):
    """
    Takes an address and retrieves the latitude longitude pair using Google's
    georeferencing API. An API key is necesary to execute the command

    Input:
        lib_dict (dict): A dictionary where keys are library names and values
            are lists of addresses.
    Output:
        df (DataFrame): A DataFrame with columns 'lib_name', 'latitude', and
            'longitude'.
    """
    # Establish connection with the API
    gmaps = googlemaps.Client(key=GEOCODING_API_KEY)

    # Define structures to store the results
    lib_name = []
    lib_addr = []
    lat = []
    lon = []

    for lib in lib_dict:
        lib_addrs = lib_dict[lib]
        for addr in lib_addrs:
            # Geocode an address (returns a list with a dict as only element)
            geocode_result = gmaps.geocode(addr)
            if geocode_result:
                # Extracting 'lat' and 'lng' from the 'location'
                data = geocode_result[0]["geometry"]
                lat.append(data["location"]["lat"])
                lon.append(data["location"]["lng"])
                lib_name.append(lib)
                lib_addr.append(addr)

    # Creates final structure
    df = pd.DataFrame(
        {
            "lib_name": lib_name,
            "lib_address": lib_addr,
            "latitude": lat,
            "longitude": lon,
        }
    )

    # Removes duplicates based on coordinates
    df = df.drop_duplicates(subset=["latitude","longitude"])
    df.reset_index().drop(columns="index",inplace=True)

    return df


if __name__ == "__main__":
    # Initial statements
    print("Enter the library type code to obtain the data:")
    lib_code = input()

    # If digit string represents an integer, cleans the data
    if lib_code.isdigit() and lib_code in LIB_CODES:
        ini_data = load_data(lib_code)
        new_data = geocode_lib(ini_data)

        # Exports the dataset
        file_name = "../data/geocoded_lib_data_" + LIB_CODES[lib_code] + ".csv"
        new_data.to_csv(file_name, index=False)
    else:
        print("Please enter a valid library code.")
