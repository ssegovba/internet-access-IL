# Retrieve data from the American Community Survey (ACS)

# This code extracts data about internet use from the ACS for the state of Illinois.

import requests
import pandas as pd
import numpy as np
from constants import ACS_KEY

class CensusAPI:
    """
    Extracts data from the US Census Data for a specified geographic location and state.
    The default is at the census tract level and for the state of Illinois.
    """

    def __init__(self, year):
        """
        Initializes a new instance of the CensusAPI class.

        Inputs:
            - year (int): An integer with the year the data want to be
              consulted
        """

        assert isinstance(year, int), f"year parameter is 'str' and should be 'int'"

        self.base_url_macro_table = (
            "https://api.census.gov/data/" + str(year) + "/acs/acs5"
        )

    def get_data(self, geo="tract:*", state="17"):
        """
        This method extracts data from the US Census Bureau API
        for the specified geographic location and state.

        Inputs:
            - geo (str): A string representing the geographic location
              to retrieve data for.
            - state (str): A string representing the state
              to retrieve data for.

        Returns:
            - dataframe (Pandas df): A DataFrame containing
              the data retrieved from the US Census Bureau API.
        """

        # First letter: Table
        # First two #: subject identifier
        # Three following #: table # within a subject
        # Three digits after _: line number within a table
        # Last letter: E for estimate, M for margin, etc.
        cols = [
            "GEO_ID",
            "NAME",
            "B28002_001E",
            "B28002_002E",
            "B28002_003E",
            "B28002_004E",
            "B28002_005E",
            "B28002_006E",
            "B28002_007E",
            "B28002_008E",
            "B28002_009E",
            "B28002_010E",
            "B28002_011E",
            "B28002_012E",
            "B28002_013E",
        ]
        #Description of variables: https://api.census.gov/data/2021/acs/acs5/variables.html

        cols = ",".join(cols)

        # Define the API calls
        full_url_macro = f"{self.base_url_macro_table}?get={cols}&for={geo}&in=state:{state}&key={ACS_KEY}"
        data_response_macro = requests.get(full_url_macro)

        macro_json = data_response_macro.json()

        #Convert JSON data to Pandas dataframes
        macro_df = pd.DataFrame(macro_json[1:], columns=macro_json[0])

        macro_df = macro_df.rename(
            columns={
                "GEO_ID": "geo_id",
                "NAME": "census_name",
                "B28002_001E": "total_hh",
                "B28002_002E": "internet_sub_hh",
                "B28002_003E": "dial_up_hh",
                "B28002_004E": "broadband_hh",
                "B28002_005E": "cellular_data_hh",
                "B28002_006E": "only_cellular_data_hh",
                "B28002_007E": "type_broadband_hh",
                "B28002_008E": "only_broadband_hh",
                "B28002_009E": "satellite_hh",
                "B28002_010E": "only_satellite_hh",
                "B28002_011E": "only_other_hh",
                "B28002_012E": "internet_without_subs_hh",
                "B28002_013E": "no_internet_hh",
            }
        )

        return self.move_key_columns_to_front(geo, macro_df)


    def move_key_columns_to_front(self, geo, dataframe):
        """
        This function moves the geo columns to the front of the table
        to improve readability

        Inputs:
        - dataframe: a Pandas df

        Returns:
        - a dataframe with re-ordered columns
        """
        dataframe = dataframe.drop(['state'], axis=1)

        if geo == "tract:*":
            cols_to_move = ["tract", "county"]
        else:
            cols_to_move = ["block group", "tract", "county"]
        
        dataframe = dataframe[
        cols_to_move + [col for col in dataframe.columns if col not in cols_to_move]
        ]

        return dataframe
    
#-------------------------------------------

#Creating an instance of the CensusAPI class

year = 2021
api = CensusAPI(year)

#Data at Tract level
df = api.get_data()
df.loc[:,"GEOID20"] = df.loc[:,"geo_id"].str[9:]

df.to_csv("../data/acs_internet_use.csv", index=False)

#Data at Block group level
df = api.get_data(geo='block%20group:*', state="17%20county:*")
df.loc[:,"GEOID20"] = df.loc[:,"geo_id"].str[9:]

df.to_csv("../data/acs_internet_use_block.csv", index=False)