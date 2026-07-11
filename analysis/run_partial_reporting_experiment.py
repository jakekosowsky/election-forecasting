import pandas as pd
df = pd.read_csv("combined_2016_2020_precincts.csv")

data = df[['PRECINCTID', 'Precinct_L', 'age_18_19', 'age_20_24',
       'age_25_29', 'age_35_44', 'age_45_54', 'age_55_64', 'age_65_74',
       'age_75_84', 'age_85over', 'party_dem', 'party_rep', 'party_npp',
       'eth1_eur', 'eth1_hisp', 'eth1_aa', 'eth1_esa', 'eth1_oth']]

size = 1000
data = data[:size]


dat2 = df[:size]

nearest_neighbors_info = []

for i in range(size):
    indices, dists = find_nearest_neighbors(total_distances, i, size)
    neighbors_info = {'precinct': i, 'nearest_indices': indices, 'distances': dists}
    nearest_neighbors_info.append(neighbors_info)


precinct_objects = []

for info in nearest_neighbors_info:
    precinct_id = info['precinct']
    
    # Retrieve estimated values from the dataset for each precinct
    estimated_dem = dat2.loc[precinct_id, 'DEM VOTE - 2016']
    estimated_rep = dat2.loc[precinct_id, 'REP VOTE - 2016']
    estimated_turnout = dat2.loc[precinct_id, 'TURNOUT - 2016']
    
    # Get nearest precincts and distances
    similar_precincts = list(zip(info['nearest_indices'], info['distances']))
    
    # Create a Precinct object
    precinct = Precinct(
        id=precinct_id,
        estimated_dem=estimated_dem,
        estimated_rep=estimated_rep,
        estimated_turnout=estimated_turnout,
        similar_precincts=similar_precincts
    )
    
    # Add to the precinct_objects list
    precinct_objects.append(precinct)

# Example Usage:
# Assuming you have created a list of Precinct objects (precinct_objects) and the data DataFrame with 2020 results.
randomly_report_precincts(precinct_objects, data, report_percentage=0.3)

calculate_adjustments(precinct_objects, hyper_parameter = 1)

# Example Usage:
# Assuming you have created a list of Precinct objects (precinct_objects) and the dat2 DataFrame with actual 2020 results
mape = compare_predicted_to_actual(precinct_objects, dat2)
