"""Prepare the Michigan precinct feature layer used by the needle model.

This module reconstructs the GeoJSON preparation workflow referenced by the
original `michigan-needle` development copy.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd


AGE_COLUMNS = [
    "age_18_19", "age_20_24", "age_25_29", "age_35_44", "age_45_54",
    "age_55_64", "age_65_74", "age_75_84", "age_85over",
]
PARTY_COLUMNS = ["party_dem", "party_rep", "party_npp"]
DEMOGRAPHIC_COLUMNS = ["eth1_eur", "eth1_hisp", "eth1_aa", "eth1_esa", "eth1_oth"]
IDENTIFIER_COLUMNS = ["PRECINCTID", "Precinct_L"]


def normalize_distributions(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Normalize a related group of count columns into row-level shares."""
    totals = frame[columns].sum(axis=1).replace(0, pd.NA)
    frame.loc[:, columns] = frame[columns].div(totals, axis=0)
    frame.loc[:, columns] = frame[columns].fillna(frame[columns].median())
    return frame


def load_precinct_features(
    path: str | Path = "data/geojson/michigan_2022.geojson",
) -> gpd.GeoDataFrame:
    """Load and normalize the demographic feature groups used for similarity."""
    precincts = gpd.read_file(path)
    columns = IDENTIFIER_COLUMNS + AGE_COLUMNS + PARTY_COLUMNS + DEMOGRAPHIC_COLUMNS
    features = precincts.loc[:, columns].copy()
    for group in [AGE_COLUMNS, PARTY_COLUMNS, DEMOGRAPHIC_COLUMNS]:
        features = normalize_distributions(features, group)
    return features
