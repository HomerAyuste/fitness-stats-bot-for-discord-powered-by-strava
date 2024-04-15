import pytest
from bot.graphs_and_stats import *
stat = stats()

@pytest.fixture
def example_df():
    my_cols =['name',
        'start_date_local',
        'type',
        'distance',
        'moving_time',
        'elapsed_time',
        'total_elevation_gain',
        'elev_high',
        'elev_low',
        'average_speed',
        'max_speed',
        'average_heartrate',
        'max_heartrate',
        'start_latitude',
        'start_longitude',
        'distance_km',
        'start_date_local',
        'day_of_week',
        'month_of_year',
        'year',
        'moving_time',
        'elapsed_time',
        'elapsed_time_hr',
        'moving_time_hr',
        'average_speed_kph',
        'max_speed_kph']
    
    df = pd.DataFrame(columns=my_cols)
    #df.loc[0] = ['','','','']
    return df

def test_cumulative_graph(example_df):
    assert isinstance(stat.cumulative_graph(example_df,"","moving_time_hr",""), File)
