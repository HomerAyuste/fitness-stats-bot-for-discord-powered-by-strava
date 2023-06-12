import time
import pandas as pd
import matplotlib.pyplot as plt
import io
from interactions import File

def recap(df):
    df1 = df.groupby(df['year'])['moving_time'].sum()
    df1.plot(kind='bar')
    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = File(data_stream, file_name='graph.png')
    return image