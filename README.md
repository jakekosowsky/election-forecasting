# Precinct-Level Election Forecasting

A prototype election “needle” that estimates outstanding vote using similarities among precincts. The project combines demographic and historical voting features, identifies comparable precincts, and updates an aggregate forecast as simulated results arrive.

## Approach

1. Prepare precinct demographics and prior-election vote shares.
2. Encode mixed feature types and reduce dimensionality.
3. measure similarity between precincts.
4. Estimate unreported precincts from their nearest reported peers.
5. Compare the evolving forecast with the final result and a simple historical baseline.

## Repository structure

- `notebooks/election_forecasting.ipynb` — modeling prototype and simulation
- `data/` — source data is excluded; see the notebook for the expected schema

## Tools

Python, pandas, NumPy, GeoPandas, scikit-learn, nearest-neighbor methods, and Jupyter.

## Limitations

This is a retrospective modeling exercise, not a live election prediction. Random reporting order is a simplifying assumption and does not reproduce the geographic and operational patterns of real vote reporting.

## Responsible use

Forecasts are sensitive to data quality, turnout assumptions, reporting bias, and model specification. Results should be treated as exploratory rather than authoritative.
