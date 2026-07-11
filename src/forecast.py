"""Aggregate reported and estimated precinct results into a forecast."""

def calculate_predicted_results(precincts):
    """
    Calculate the predicted election results by aggregating Democratic and Republican votes 
    across all precincts, using actual results if reported, otherwise using estimated results.
    
    :param precincts: List of Precinct objects
    :return: Predicted total Democratic votes, Republican votes
    """
    total_dem_votes = 0
    total_rep_votes = 0

    for precinct in precincts:
        if precinct.reported:
            # Use actual reported results if precinct has reported
            dem_votes = precinct.actual_dem * precinct.actual_turnout
            rep_votes = precinct.actual_rep * precinct.actual_turnout
        else:
            # Use estimated results if precinct has not reported
            dem_votes = precinct.adjusted_dem * precinct.adjusted_turnout
            rep_votes = precinct.adjusted_rep * precinct.adjusted_turnout

        # Aggregate the votes
        total_dem_votes += dem_votes
        total_rep_votes += rep_votes

    return total_dem_votes, total_rep_votes

def calculate_actual_results(dat2):
    """
    Aggregate the actual 2020 election results from the 'dat2' DataFrame, where 
    '2020_actual_dem_votes' and '2020_actual_rep_votes' are proportions.
    
    :param dat2: DataFrame containing true 2020 election results with proportions 
                 for Democratic and Republican votes, and total turnout
    :return: Total Democratic votes, Republican votes
    """
    # Calculate actual votes by multiplying proportions by the total turnout for each precinct
    total_actual_dem_votes = (dat2['DEM VOTE - 2020'] * dat2['TURNOUT - 2020']).sum()
    total_actual_rep_votes = (dat2['REP VOTE - 2020'] * dat2['TURNOUT - 2020']).sum()

    return total_actual_dem_votes, total_actual_rep_votes

def calculate_mape(predicted_dem, predicted_rep, actual_dem, actual_rep):
    """
    Calculate the mean absolute percentage error (MAPE) between predicted and actual results
    for Democratic and Republican votes.
    
    :param predicted_dem: Total predicted Democratic votes
    :param predicted_rep: Total predicted Republican votes
    :param actual_dem: Total actual Democratic votes
    :param actual_rep: Total actual Republican votes
    :return: MAPE (mean absolute percentage error)
    """
    dem_mape = abs((actual_dem - predicted_dem) / actual_dem) * 100
    rep_mape = abs((actual_rep - predicted_rep) / actual_rep) * 100
    overall_mape = (dem_mape + rep_mape) / 2
    return overall_mape

def compare_predicted_to_actual(precincts, dat2):
    """
    Compare the predicted election results to the actual 2020 election results and 
    calculate the mean absolute percentage error (MAPE) for Democratic and Republican votes.
    
    :param precincts: List of Precinct objects with predicted results
    :param dat2: DataFrame containing actual 2020 election results
    """
    # Calculate predicted results using the precinct objects
    predicted_dem, predicted_rep = calculate_predicted_results(precincts)
    
    # Calculate actual results using the dat2 DataFrame
    actual_dem, actual_rep = calculate_actual_results(dat2)
    
    # Calculate predicted and actual percentages
    total_predicted_votes = predicted_dem + predicted_rep
    total_actual_votes = actual_dem + actual_rep

    predicted_dem_percentage = (predicted_dem / total_predicted_votes) * 100
    predicted_rep_percentage = (predicted_rep / total_predicted_votes) * 100
    
    actual_dem_percentage = (actual_dem / total_actual_votes) * 100
    actual_rep_percentage = (actual_rep / total_actual_votes) * 100
    
    # Calculate MAPE between predicted and actual results
    mape = calculate_mape(predicted_dem, predicted_rep, actual_dem, actual_rep)
    
    # Output the comparison of predicted vs. actual results
    print("Comparison of Predicted vs. Actual Results:")
    print(f"Predicted Democratic Votes: {predicted_dem:.0f} ({predicted_dem_percentage:.2f}%)")
    print(f"Predicted Republican Votes: {predicted_rep:.0f} ({predicted_rep_percentage:.2f}%)")
    
    print("\nActual 2020 Results:")
    print(f"Actual Democratic Votes: {actual_dem:.0f} ({actual_dem_percentage:.2f}%)")
    print(f"Actual Republican Votes: {actual_rep:.0f} ({actual_rep_percentage:.2f}%)")
    
    # Output the MAPE (mean absolute percentage error)
    print(f"\nMean Absolute Percentage Error (MAPE): {mape:.2f}%")
    return mape




def calculate_projected_2016_results(dat2):
    """
    Calculate projected 2020 election results if 2016 Democratic and Republican vote proportions
    held exactly the same in 2020.
    
    :param dat2: DataFrame containing 2016 vote proportions and 2020 total turnout
    :return: Projected total Democratic votes, Republican votes based on 2016 proportions
    """
    # Use 2016 proportions multiplied by 2020 total turnout to project 2020 votes
    projected_dem_votes = (dat2['DEM VOTE - 2016'] * dat2['TURNOUT - 2020']).sum()
    projected_rep_votes = (dat2['REP VOTE - 2016'] * dat2['TURNOUT - 2020']).sum()
    
    return projected_dem_votes, projected_rep_votes

def compare_projected_2016_to_actual(dat2):
    """
    Compare projected 2020 election results (if 2016 proportions held) to the actual 2020 results.
    
    :param dat2: DataFrame containing 2016 vote proportions and actual 2020 results
    """
    # Calculate projected results assuming 2016 proportions hold
    projected_dem, projected_rep = calculate_projected_2016_results(dat2)
    
    # Calculate actual results from the dat2 DataFrame
    actual_dem, actual_rep = calculate_actual_results(dat2)
    
    # Calculate projected and actual percentages
    total_projected_votes = projected_dem + projected_rep
    total_actual_votes = actual_dem + actual_rep

    projected_dem_percentage = (projected_dem / total_projected_votes) * 100
    projected_rep_percentage = (projected_rep / total_projected_votes) * 100
    
    actual_dem_percentage = (actual_dem / total_actual_votes) * 100
    actual_rep_percentage = (actual_rep / total_actual_votes) * 100
    
    # Output the comparison of projected 2016 results vs. actual 2020 results
    print("Comparison of Projected 2016 Results (Applied to 2020 Turnout) vs. Actual 2020 Results:")
    print(f"Projected Democratic Votes (2016 Proportions): {projected_dem:.0f} ({projected_dem_percentage:.2f}%)")
    print(f"Projected Republican Votes (2016 Proportions): {projected_rep:.0f} ({projected_rep_percentage:.2f}%)")
    
    print("\nActual 2020 Results:")
    print(f"Actual Democratic Votes: {actual_dem:.0f} ({actual_dem_percentage:.2f}%)")
    print(f"Actual Republican Votes: {actual_rep:.0f} ({actual_rep_percentage:.2f}%)")
    
compare_projected_2016_to_actual(dat2)
