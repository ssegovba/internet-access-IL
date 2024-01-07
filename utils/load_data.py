import sys
import os

sys.path.append(os.path.abspath(".."))

import pandas as pd
import geopandas as gpd

DATA_PATH = "../data/"


def load_data_sources():
    # 1. Loading Data

    boundaries = gpd.read_file(DATA_PATH + "tl_2020_17_tract20/tl_2020_17_tract20.shp")
    libs_data = pd.read_csv(DATA_PATH + "lib_data_plot.csv")
    acs_data = pd.read_csv(DATA_PATH + "acs_internet_use.csv")
    fcc_data = pd.read_csv(DATA_PATH + "fcc_data_agg.csv")

    # 2. Using the `acs_data`, we create the broadband access variables

    acs_data.loc[:, "share_broadband"] = (
        acs_data.loc[:, "only_broadband_hh"] * 100 / acs_data.loc[:, "total_hh"]
    )
    acs_data.loc[:, "share_cellular"] = (
        acs_data.loc[:, "only_cellular_data_hh"] * 100 / acs_data.loc[:, "total_hh"]
    )
    acs_data.loc[:, "share_satellite"] = (
        acs_data.loc[:, "only_satellite_hh"] * 100 / acs_data.loc[:, "total_hh"]
    )
    acs_data.loc[:, "share_no_internet"] = (
        acs_data.loc[:, "no_internet_hh"] * 100 / acs_data.loc[:, "total_hh"]
    )
    acs_data = acs_data.loc[acs_data.loc[:, "total_hh"] != 0,]
    acs_data.loc[:, "GEOID20"] = acs_data.loc[:, "GEOID20"].astype(str)

    return acs_data, fcc_data, libs_data, boundaries
