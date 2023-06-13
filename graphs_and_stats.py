import time
import pandas as pd
import matplotlib.pyplot as plt
import io
from interactions import File

def recap(df, title, column='month_and_year', y_column='moving_time_hr'):
    if column =='month_and_year':
        df[column] = df['month_of_year'].map(str) + '-' + df['year'].map(str)
        df[column] = pd.to_datetime(df[column],format='%m-%Y')
        df[column] = df[column].dt.strftime('%y-%m')
    df1 = df.groupby(df[column].values)[y_column].sum()
    df1.plot(kind='bar')
    plt.title(title)
    plt.ylabel('Hours' if y_column=='moving_time_hr' else 'Distance (m)')
    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')

    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image