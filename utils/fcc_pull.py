# Retrieve data from the US National Broadband map using Virginia Tech API

import requests
import pandas as pd
from io import BytesIO
import zipfile
from constants import FCC_TOKEN
import os

# API class


class USBroadbandMapAPI:
    """
    This class extracts broadband data of the US National Broadband map for Illinois
    using the API created by the Spin Lab at Virginia Tech.
    """

    def __init__(self, token):
        """
        This function initializes a new instance of the USBroadbandMapAPI class

        Inputs:
            - token (str): a string representing the API token needed to access
            US Broadban Map API. It can be obtained by requesting it to nbmarchive@vt.edu.
        """

        self.token = token
        self.base_url = "https://spin.cs.vt.edu/nbmarchive/api/query?"  # FYI LINK IN WEBPAGE HAS A TYPO: SNIP INSTEAD OF SPIN

    def get_data(self, state_abb, edition, snapshot, extraction_path):
        """
        This method extracts data from the US Broadband Map API for the
        specified state, dates and format.

        Input:
            - state_abb (str): USPS state abbreviation. Can specify multiple values.
            - edition (str): Specify the edition in YYYYMMDD format.A new edition of
                the National Broadband Map is released every six months, on June 30 and Dec 31.
            - snapshot (str): Specify the snapshot in YYYYMMDD format. About every two weeks,
                the FCC releases a new snapshot of previously released editions, reflecting
                changes since original publication.
            - extraction_path (str): specify the directory where you want to save csv file

        Returns:
            - None. Saves csv file in specified path.
        """

        full_url = f"{self.base_url}state_usps={state_abb}&edition={edition}&snapshot={snapshot}"

        response = requests.get(full_url, params={"api_key": self.token})

        if response == 200:
            # Use BytesIO to create a file-like object from the response content
            zip_file = zipfile.ZipFile(BytesIO(response.content))

            # Extract all the contents of the ZIP file
            zip_file.extractall(extraction_path)


# ----------------------------------

# API call

fcc_api = USBroadbandMapAPI(FCC_TOKEN)

fcc_api.get_data(
    state_abb="IL", edition="20221231", snapshot="20230926", extraction_path="../data"
)
