import time
import pandas as pd
import matplotlib.pyplot as plt
import io
from interactions import File

def recap(df):
    # df['month_and_year'] = df['month_of_year'].map(str) + '-' + df['year'].map(str)
    # df['month_and_year'] = pd.to_datetime(df['month_and_year'],format='%m-%Y')
    df1 = df.groupby(df['year'].values)['moving_time_hr'].sum()
    df1.plot(kind='bar')
    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image