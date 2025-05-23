import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import seaborn as sns
from interactions import File
from interactions import EmbedField
import numpy as np
import itertools
import datetime as dt
from math import floor


class stats:
    def save_graph(self):
        #save image in data stream
        data_stream = io.BytesIO()
        #plt.figure(figsize=(10,6))
        plt.savefig(data_stream,format='png')

        plt.close()
        data_stream.seek(0)
        image = File(data_stream, file_name='graph.png')
        return image

    def recap(self, df : pd.DataFrame, title : str,activity : str, column='month_and_year', y_column='moving_time_hr')-> File:

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
        image = self.save_graph()
        return image

    def distweek(self, df : pd.DataFrame,activities : str,title :str)->File:
        day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
        g = sns.catplot(x='day_of_week', y='distance_km', kind='strip',
                        data=df if activities=='' else df.loc[df['type']==activities],
                        order=day_of_week_order, col='type', height=5, aspect=1, palette='pastel')
        (g.set_axis_labels("Week day", "Distance (km)")
        .set_titles("Activity type: {col_name}")
        .set_xticklabels(rotation=30))
        g.fig.subplots_adjust(top=.9)
        g.fig.suptitle(title)

        image = self.save_graph()
        return image

    def boxplots(self, df:pd.DataFrame):

        image = self.save_graph()
        return image

    def distance_leaderboard(self):
        return

    def linegraph(self, df:pd.DataFrame, activity,limit,period, measurement):
        if activity != None:
            df = df.loc[df.type == activity]
        x = df.starting_date_local
        y = df[measurement]
        plt.plot(x,y)
        return

    def cumulative_graph(self, df:pd.DataFrame, activity:str, measurement:str, title:str)->File:
        #iterate through each year
        for year in range(df['year'].min(),df['year'].max()+1):
            df1 = df.loc[df.year==year] if activity == '' else df.loc[(df.year==year) & (df.type==activity)]
            year_data = [0] * 366
            for i in df1.index:
                year_data[df1['start_date_local'][i].timetuple().tm_yday] += df1[measurement][i]
            accum_data = list(itertools.accumulate(year_data))
            # Remove additional zeros from end of data if year is the current year
            if year == dt.datetime.now().year:
                accum_data = accum_data[0:accum_data.index(max(accum_data))]
            print(year)
            plt.plot(list(range(1,len(accum_data)+1)),accum_data,label=year)
        plt.legend()
        plt.title(title)
        plt.xlabel('Days')
        ylabel = ''
        match measurement:
            case 'moving_time_hr':
                ylabel = "Activity Duration (hours)"
            case 'distance_km':
                ylabel = "Activity Distance (km)"
            case 'total_elevation_gain':
                ylabel = "Activity Elevation Gain (m)"
        plt.ylabel(ylabel)
        plt.grid(axis='y')
        image = self.save_graph()
        return image

    def statistics(self, df : pd.DataFrame, activities : str)->list[EmbedField]:
        if activities != '':
            df = df.loc[df.type==activities]
        tot_hours = df["elapsed_time_hr"].sum()
        hours = floor(tot_hours)
        minutes = floor((tot_hours-hours)*60)
        max_dist = df["distance_km"].max()
        max_speed = df["average_speed_kph"].max()
        fields = []
        fields.append(EmbedField('Total Distance:',f'`{df["distance_km"].sum():>6,.2f} km`',True))
        fields.append(EmbedField(':stopwatch: Total Time:', f'`{hours:>6,d}:{minutes:02d} hours`',True))
        fields.append(EmbedField(':mountain_snow: Total Elevation Gain:', f'`{df["total_elevation_gain"].sum():>6,.2f} metres`', True))
        fields.append(EmbedField('Average Distance of Each Activity:', f'`{df["distance_km"].mean():>6.2f} km`', True))
        tot_hours = df["elapsed_time_hr"].mean()
        hours = floor(tot_hours)
        minutes = floor((tot_hours-hours)*60)
        fields.append(EmbedField(':stopwatch: Average Time of Each Activity:', f'`{hours:>6,d}:{minutes:02d} hours`', True))
        fields.append(EmbedField(':mountain_snow: Average Climb of Each Activity:', f'`{df["total_elevation_gain"].mean():>6.2f} metres`', True))
        fields.append(EmbedField("Overall Average Pace/Speed of Each Activity: ", f'`{df["average_speed_kph"].mean():>6.2f} km/h`'))
        fields.append(EmbedField('Best Average Pace/Speed in an Activity:',f'`{max_speed:>6.2f} km/h` - {df["start_date_local"].loc[df.average_speed_kph == max_speed].iloc[0].strftime("%b %-d %Y")}', True))
        fields.append(EmbedField('Longest Activity by Distance:',f'`{max_dist:>6.2f} km` - {df["start_date_local"].loc[df.distance_km == max_dist].iloc[0].strftime("%b %-d %Y")}', True))
        return fields