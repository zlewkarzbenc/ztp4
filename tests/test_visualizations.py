from visualizations import *
import pytest
import pandas as pd
from compute_averages import count_days_over_treshold

@pytest.fixture(scope="session")
def monthly_df():
   df = pd.DataFrame({"year": [2015, 2018, 2018, 2021],
                       "month": [1, 2, 3, 4],
                       "Warszawa": [1.3, 20, 30, 5],
                        "Katowice": [4.2, 15, 3.1, 10],
                        "Lublin": [3.4, 8.1, 1.2, 2]})
   return df

@pytest.fixture(scope="session")
def data():
    return pd.DataFrame({"Kod stacji": ["2015-01-01 12:00:00",
                                        "2015-01-01 13:00:00",
                                        "2015-01-02 12:00:00",
                                        "2015-01-03 12:00:00",
                                        "2018-01-03 13:00:00",
                                        "2018-01-03 13:00:00"],
                         "Rok": [2015, 2015, 2015, 2015, 2018, 2018],
                         ("Warszawa", "WAR"): [25, 1, 9, 10, 16, 24],
                         ("Kraków", "KRA"): [4, 16, 10, 15, 18, 19]})

def test_heatmap_run_without_err(monthly_df):
   fig = heatmaps(monthly_df)
   assert fig is not None

def test_city_trends_run_without_err(monthly_df):
   df = monthly_df.set_index(["year", "month"])
   fig = plot_city_trends(df, cities=["Warszawa", "Katowice"], years=[2015, 2018], ylim=[0, 75])
   assert fig is not None

def test_pm25_exceedance_run_without_err(data):
    exceedance_counts = count_days_over_treshold(data, treshold=15)
    fig = plot_pm25_exceedance_bars(exceedance_counts, top_n=1, base_year=2015,threshold=15)
    assert fig is not None
