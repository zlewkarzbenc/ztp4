from visualizations import *

@pytest.fixture
def monthly_df():
   monthly_df = pd.read_csv("monthly_average.csv")
   return monthly_df

def test_heatmap_run_without_err(monthly_df):
    heatmaps(monthly_df)

def test_heatmap_if_every_location(monthly_df):
    fig = heatmaps(monthly_df)
    locations = [c for c in monthly_df.columns if c not in ["year", "month"]]
    assert len(fig.data) == len(locations)
