"""
Aggregates FCC's Broadband Data

This code uses the data from the FCC to create a csv file that contains
broadband data by hexagon.
"""

import pandas as pd
import geopandas as gpd
import h3
from shapely.geometry import Polygon


def export_data(in_path: str, out_path: str) -> pd.DataFrame:
    """
    Args:

    Return:

    """

    df = pd.read_csv(in_path, index_col=False)

    df_agg = (
        df.groupby("h3_res8_id")
        .agg(
            {
                "brand_name": "nunique",
                "max_advertised_download_speed": "mean",
                "max_advertised_upload_speed": "mean",
            }
        )
        .reset_index()
    )

    agg_names = {
        "brand_name": "avg_num_providers",
        "max_advertised_download_speed": "avg_max_down_speed",
        "max_advertised_upload_speed": "avg_max_up_speed",
    }

    df_agg.rename(columns=agg_names, inplace=True)

    df_agg.loc[:, "geometry"] = df_agg.loc[:, "h3_res8_id"].apply(h3_to_polygon)

    df_agg.to_csv(out_path, index=False)


def h3_to_polygon(h3_index):
    # Get the vertices of the hexagon
    vertices = h3.h3_to_geo_boundary(h3_index)
    # Convert to (lon, lat) pairs
    vertices = [(lon, lat) for lat, lon in vertices]
    # Create and return a shapely Polygon
    return Polygon(vertices)


# -------------------------------
# Creating fcc_data_agg.csv

export_data("../data/FCC_broadband_IL.csv", "../data/fcc_data_agg.csv")
