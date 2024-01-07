"""
Merge Datasets

This script takes data from the ACS, FCC, and libraries locations to create a
single geodataframe that contains data on libraries's broadband access.

The code is specific for this analysis so it is not generalizable for other
data sets.
"""

import pandas as pd
import geopandas as gpd
from shapely import wkt


def from_df_to_gdf(df: pd.DataFrame, geom_var: bool) -> gpd.GeoDataFrame:
    """
    This function converts a df to a geodf based on a latitude, longitude pairs
    The CRS assigned is NAD83.

    Agrs:
        df: a pd.DataFrame
        geom_var: True if the df contains a "geometry" variable. False otherwise

    Returns:
        geo_df: a gpd.GeoDataFrame
    """

    # Check correct data type
    assert isinstance(geom_var, bool), f"geom_var should be a boolean"

    # Convert the df
    if geom_var:
        geo_df = gpd.GeoDataFrame(df, geometry="geometry")
    else:
        lng_col = df.loc[:, "longitude"]
        lat_col = df.loc[:, "latitude"]
        geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(lng_col, lat_col))

    # Assign CRS if non existent:
    if geo_df.crs == None:
        geo_df.crs = "EPSG:4269"

    return geo_df


def merge_gdf(
    acs_df: pd.DataFrame,
    fcc_df: pd.DataFrame,
    lib_df: pd.DataFrame,
    bound_gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    This function merges the datasets used for the analysis and outputs a
    single one with the relevant variables.

    Args:
        acs_df: dataframe containing data from the ACS
        fcc_df: dataframe containing data from the ACS
        lib_df: dataframe containing data from the libraries in IL
        bound_gdf: dataframe containing data from census tract boundaries in IL

    Returns:
        merged_gdf: a gpd.GeoDataFrame
        acs_gdf: a gpd.GeoDataFrame
        fcc_gdf: a gpd.GeoDataFrame
        lib_gdf: a gpd.GeoDataFrame
    """

    # ACS DATA AND BOUNDARIES
    cols_acs = [
        "tract",
        "county",
        "GEOID20",
        "share_broadband",
        "share_cellular",
        "share_satellite",
        "share_no_internet",
    ]
    cols_bound = ["GEOID20", "geometry"]
    acs_gdf = pd.merge(
        acs_df.loc[:, cols_acs],
        bound_gdf.loc[:, cols_bound],
        on="GEOID20",
        how="inner",
    )

    # Convert acs_gdf to gdf
    acs_gdf = from_df_to_gdf(acs_gdf, True)

    # LIBRARY DATA AND BOUNDARIES
    lib_gdf = from_df_to_gdf(lib_df, False)
    lib_gdf = gpd.sjoin(
        lib_gdf, bound_gdf.loc[:, cols_bound], how="left", predicate="intersects"
    )
    lib_gdf.drop("index_right", axis=1, inplace=True)

    # LIBRARY DATA AND ACS DATA (MERGED DATA)
    merged_gdf = pd.merge(lib_gdf, acs_gdf.loc[:, cols_acs], on="GEOID20", how="inner")

    # MERGED DATA AND FCC DATA
    fcc_df.loc[:, "geometry"] = fcc_df.loc[:, "geometry"].apply(wkt.loads)
    fcc_gdf = from_df_to_gdf(fcc_df, True)
    merged_gdf = gpd.sjoin(merged_gdf, fcc_gdf, how="left", predicate="intersects")
    merged_gdf.drop(["index_right", "h3_res8_id"], axis=1, inplace=True)

    return merged_gdf, acs_gdf, fcc_gdf, lib_gdf
