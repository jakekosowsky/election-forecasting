# Election-Night Forecasting from Partial Precinct Returns

How much can a small amount of reported vote tell us about everything that has not reported yet?

This project simulates election night as a stream of partial precinct returns. When early results arrive, the model finds historically and demographically similar precincts, measures how those reported precincts are deviating from their baseline, and extrapolates that movement to precincts still outstanding.

## Josh Shapiro election analysis

The repository consolidates the precinct modeling work associated with the Josh Shapiro campaign analysis into one public project: the combined precinct dataset, similarity model, live adjustment logic, reporting simulation, evaluation code, and the original research notebook.

## Model design

1. Represent each precinct through age, party-registration, and demographic distributions.
2. Measure similarity with Jensen–Shannon divergence.
3. Identify the most comparable precincts for every reporting unit.
4. Simulate a small share of precincts reporting actual results.
5. Measure each reported precinct's change from the historical baseline.
6. Transfer weighted changes to similar outstanding precincts.
7. Aggregate reported and estimated vote into a statewide forecast.
8. Compare the evolving prediction with the final result and a historical baseline.

## Repository structure

```text
src/
  similarity.py     demographic distance and nearest-neighbor logic
  precinct.py       precinct state and live-result adjustments
  forecast.py       aggregation, baselines, and forecast error
  simulation.py     partial reporting and parameter evaluation
analysis/
  run_partial_reporting_experiment.py
data/
  combined_2016_2020_precincts.csv
notebooks/
  election_forecasting.ipynb
```

## Interpretation

The central idea is not to treat early vote totals as representative of the whole electorate. It asks which kinds of precincts have reported, learns the size and direction of their change, and applies that signal only to genuinely comparable places.

## Tools

Python · pandas · NumPy · SciPy · scikit-learn · GeoPandas · nearest-neighbor modeling
