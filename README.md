# Election-Night Forecasting from Partial Precinct Returns

How much can a small amount of reported vote tell us about the final election outcome?

This project shows how even a small share of incoming precinct returns can support a useful prediction of the final result. It simulates election night as a stream of partial returns, learns from the places that have reported, and extrapolates that evidence to the places still outstanding.

## Model design

1. Build a historical baseline for every precinct using past results and demographic data.
2. Ingest the small set of precincts that have reported so far.
3. Compare those new results with what history suggested for similar places.
4. Extrapolate the observed changes to comparable precincts that have not reported.
5. Combine reported and estimated votes into a final election forecast, then evaluate it against the completed result.

## Repository structure

```text
src/
  geojson_precinct_features.py  precinct feature preparation
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

The central idea is not to treat early vote totals as representative of the whole electorate. The model asks which kinds of precincts have reported, measures how their results compare with historical expectations, and applies that signal only to genuinely comparable places. The simulation demonstrates that partial returns can predict the eventual outcome well before every precinct has reported.

## Tools

Python · pandas · NumPy · SciPy · scikit-learn · GeoPandas · nearest-neighbor modeling
