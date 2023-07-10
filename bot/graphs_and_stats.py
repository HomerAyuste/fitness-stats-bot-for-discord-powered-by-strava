import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import seaborn as sns
from interactions import File
import numpy as np
import itertools
import datetime as dt

def save_graph():
    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')

    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image

def recap(df : pd.DataFrame, title : str,activity, column='month_and_year', y_column='moving_time_hr'):

    if column =='month_and_year':
        df[column] = df['month_of_year'].map(str) + '-' + df['year'].map(str)
        df[column] = pd.to_datetime(df[column],format='%m-%Y')
        df[column] = df[column].dt.strftime('%y-%m')
    if y_column =='distance':
        df.distance = df.distance/1000
    df1 = df.groupby(df[column].values)[y_column].sum()
    ax = df1.plot(kind='bar')
    ax.set_axisbelow(True)
    plt.title(title)
    plt.ylabel('Hours' if y_column=='moving_time_hr' else 'Distance (km)')
    plt.grid(axis='y')
    image = save_graph()
    return image

def distweek(df : pd.DataFrame,activities : str,title :str):
    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    g = sns.catplot(x='day_of_week', y='distance_km', kind='strip',
                    data=df if activities=='' else df.loc[df['type']==activities],
                    order=day_of_week_order, col='type', height=5, aspect=1, palette='pastel')
    (g.set_axis_labels("Week day", "Distance (km)")
    .set_titles("Activity type: {col_name}")
    .set_xticklabels(rotation=30))
    g.fig.subplots_adjust(top=.9)
    g.fig.suptitle(title)

    image = save_graph()
    return image

def boxplots(df:pd.DataFrame):

    image = save_graph()
    return image

def distance_leaderboard():
    return

def linegraph(df:pd.DataFrame,activity,limit,period, measurement):
    if activity != None:
        df = df.loc[df.type == activity]
    x = df.starting_date_local
    y = df[measurement]
    plt.plot(x,y)
    return

def cumulative_graph(df:pd.DataFrame, activity:str, measurement:str, title:str):
    fig, ax = plt.subplots(1)
    #iterate through each year
    for year in range(df['year'].min(),df['year'].max()+1):
        df1 = df.loc[df.year==year] if activity == '' else df.loc[df.year==year & df.activity==activity]
        year_data = [0] * 366
        for i in df1.index:
            year_data[df1['start_date_local'][i].timetuple().tm_yday] += df1[measurement][i]
        accum_data = list(itertools.accumulate(year_data))
        # Remove additional zeros from end of data is if year is the current year
        if year == dt.datetime.now().year:
            accum_data = accum_data[0:accum_data.index(max(accum_data))]
        ax.plot(list(range(1,len(accum_data)+1)),accum_data,'-',label=year)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel('Days')
    ylabel = 'Activity Duration (Hours)' if measurement=='elapsed_time_hr' else 'Activity Distance (km)'
    ax.set_ylabel(ylabel)
    ax.grid(axis='y')
    image = save_graph()
    return image