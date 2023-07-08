import pandas as pd
import matplotlib.pyplot as plt
import io
import seaborn as sns
from interactions import File

def recap(df, title,activity, column='month_and_year', y_column='moving_time_hr'):

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
    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')

    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image

def distweek(df,activities,title):
    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    g = sns.catplot(x='day_of_week', y='distance_km', kind='strip',
                    data=df if activities=='' else df.loc[df['type']==activities],
                    order=day_of_week_order, col='type', height=5, aspect=1, palette='pastel')
    (g.set_axis_labels("Week day", "Distance (km)")
    .set_titles("Activity type: {col_name}")
    .set_xticklabels(rotation=30))
    g.fig.subplots_adjust(top=.9)
    g.fig.suptitle(title)

    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image

def boxplots(df):

    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image

def distance_leaderboard():
    return

def linegraph(df,activity,limit,period, measurement):
    if activity != None:
        df = df.loc[df.type == activity]
    x = df.starting_date_local
    y = df[measurement]
    plt.plot(x,y)
    return

def cumulative_graph(df, activity, measurement):
    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image