"""Simulate partial reporting and evaluate forecast calibration."""

import random

def randomly_report_precincts(precincts, data, report_percentage=0.3):
    """
    Randomly chooses 30% of the precincts and reports their actual data from the 2020 columns.
    
    :param precincts: List of Precinct objects
    :param data: DataFrame containing actual results with 2020 column names
    :param report_percentage: Percentage of precincts to report (default is 30%)
    """
    num_precincts = len(precincts)
    num_to_report = int(num_precincts * report_percentage)

    # Randomly select 30% of the precincts
    selected_indices = random.sample(range(num_precincts), num_to_report)
    
    for i in selected_indices:
        precinct = precincts[i]
        
        # Extract actual data for this precinct from the 2020 columns
        actual_dem = dat2.loc[precinct.id, 'DEM VOTE - 2020']  # Assuming '2020_actual_dem' column
        actual_rep = dat2.loc[precinct.id, 'REP VOTE - 2020']  # Assuming '2020_actual_rep' column
        actual_turnout = dat2.loc[precinct.id, 'TURNOUT - 2020']  # Assuming '2020_actual_turnout' column
        
        # Report the actual results
        update_precinct_results(precinct, actual_dem, actual_rep, actual_turnout)
        




def instantiate_precinct_objects(nearest_neighbors_info, dat2):
    """ Re-instantiate the precinct objects from nearest neighbors info and data. """
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
    
    return precinct_objects

def test_hyperparameters(nearest_neighbors_info, dat2, data, report_percentage=0.1, trials=20):
    """
    Test different hyperparameters between 0 and 1 and return the corresponding average MAPE for each hyperparameter.
    
    :param nearest_neighbors_info: Information to build the precinct objects
    :param dat2: DataFrame containing actual and estimated 2016/2020 results
    :param data: DataFrame for actual reporting
    :param report_percentage: Percentage of precincts to randomly report
    :param trials: Number of times to test each hyperparameter
    :return: Dictionary of hyperparameters and their corresponding average MAPE
    """
    hyperparameter_results = {}

    # Range of hyperparameters between 0 and 1
    hyperparameter_values = np.linspace(0.85, 0.95, 11)

    for hyperparameter in hyperparameter_values:
        mape_values = []
        
        # Test each hyperparameter value over multiple trials
        for _ in range(trials):
            # Re-instantiate precinct objects for each trial
            precinct_objects = instantiate_precinct_objects(nearest_neighbors_info, dat2)
            
            # Randomly report precincts
            randomly_report_precincts(precinct_objects, data, report_percentage)
            
            # Calculate adjustments using the current hyperparameter
            calculate_adjustments(precinct_objects, hyper_parameter=hyperparameter)
            
            # Calculate MAPE
            mape = compare_predicted_to_actual(precinct_objects, dat2)
            mape_values.append(mape)

        # Calculate average MAPE for this hyperparameter
        average_mape = np.mean(mape_values)
        
        # Store the hyperparameter and its average MAPE
        hyperparameter_results[hyperparameter] = average_mape

    return hyperparameter_results

# Example Usage:
# Assuming you have created the nearest_neighbors_info and the dat2 DataFrame
hyperparameter_results = test_hyperparameters(nearest_neighbors_info, dat2, data)

# Print the hyperparameters and their corresponding average MAPE
for hyperparameter, average_mape in hyperparameter_results.items():
    print(f"Hyperparameter: {hyperparameter:.2f}, Average MAPE: {average_mape:.4f}")
