"""Build demographic similarity matrices between precincts."""

import geopandas as gpd
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

from scipy.spatial import distance
from sklearn.metrics import pairwise_distances
from scipy.stats import entropy
import numpy as np



AGE_CATEGORIES = ['age_18_19', 'age_20_24' ,'age_25_29', 'age_35_44', 'age_45_54', 'age_55_64', 'age_65_74', 'age_75_84', 'age_85over']
PARTY_ID_CATEGORIES = ['party_dem', 'party_rep', 'party_npp']
DEMOGRAPHIC_CATEGORIES = ['eth1_eur', 'eth1_hisp', 'eth1_aa', 'eth1_esa', 'eth1_oth']


total_filters = ['PRECINCTID', 'Precinct_L'] + AGE_CATEGORIES + PARTY_ID_CATEGORIES + DEMOGRAPHIC_CATEGORIES

all_categorical_features = AGE_CATEGORIES + PARTY_ID_CATEGORIES + DEMOGRAPHIC_CATEGORIES

# Note: in MI eth1_oth is likely arab voters
DEMOGRAPHIC_CATEGORIES = ['eth1_eur', 'eth1_hisp', 'eth1_aa', 'eth1_esa', 'eth1_oth']

# Function to calculate Jensen-Shannon Divergence
def jensen_shannon_divergence(p, q):
    m = 0.5 * (p + q)
    return 0.5 * (entropy(p, m) + entropy(q, m))

# Compute pairwise Jensen-Shannon Divergence for each category
def compute_category_distances(data, categories):
    # Normalize data if not already percentages
    data_normalized = data[categories].div(data[categories].sum(axis=1), axis=0)
    dist_matrix = pairwise_distances(data_normalized, metric=lambda x, y: jensen_shannon_divergence(x, y))
    return dist_matrix

# Compute distances for each category
age_distances = compute_category_distances(data, AGE_CATEGORIES)
party_distances = compute_category_distances(data, PARTY_ID_CATEGORIES)
demographic_distances = compute_category_distances(data, DEMOGRAPHIC_CATEGORIES)

# Aggregate these distances (simple average)
total_distances = (age_distances + party_distances + demographic_distances) / 3

# Find nearest neighbors manually
def find_nearest_neighbors(dist_matrix, index, n_neighbors=10):
    distances = dist_matrix[index]
    valid_indices = np.where(distances != 0)[0]  # Get indices where distance is not 0
    sorted_indices = np.argsort(distances[valid_indices])  # Sort based on distances, ignoring zeroes
    nearest_indices = valid_indices[sorted_indices][:n_neighbors]  # Get the top n_neighbors
    return nearest_indices, distances[nearest_indices]
