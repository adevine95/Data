#%%
import pandas as pd
import folium
import datetime 
import numpy as np
from sympy.plotting.tests.test_plot import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#%%
df_static = pd.read_csv('dublin.csv')
df = pd.read_csv('dublinbikes_20211001_20220101_CLEANTIME.gz')

#%%
'''
Clean column names and split out times
'''
df1=df
df1 = df1.drop(['Unnamed: 0', 
          'LAST UPDATED', 
          'STATUS',
          'ADDRESS',
          'LATITUDE',
          'LONGITUDE'],axis =1)

df1.rename(columns=
           {'STATION ID':'id',
            'TIME':'time', 
            'NAME':'name',
            'BIKE STANDS':'no_stands', 
            'AVAILABLE BIKE STANDS':'free_stands', 
            'AVAILABLE BIKES':'free_bikes'
            },inplace=True)
df1['proportion_filled'] = (df1['free_bikes']/df1['no_stands'])*100

#Change times from strings to datetimes
df1['time']= pd.to_datetime((df1['time']),format ='%Y-%m-%d %H:%M:%S.%f' )
#split out individual time attributes 
df1['year'] = pd.DatetimeIndex(df1['time']).year
df1['month'] = pd.DatetimeIndex(df1['time']).month
df1['hour'] = pd.DatetimeIndex(df1['time']).hour
df1['time_of_day'] = pd.DatetimeIndex(df1['time']).hour
df1['minute'] = pd.DatetimeIndex(df1['time']).minute
df1['day_num'] = pd.DatetimeIndex(df1['time']).weekday
df1['day_name'] = pd.DatetimeIndex(df1['time']).weekday
df1['workday'] = pd.DatetimeIndex(df1['time']).weekday

#rename some data using dictionaries
day_str = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
day_num = (0,1,2,3,4,5,6)
day_zip = zip(day_num,day_str)
day_list= list(day_zip)
day_dict = dict(day_list)

workday_str = ('midweek','midweek','midweek','midweek','midweek','weekend','weekend')
workday_zip = zip(day_num,workday_str)
workday_list= list(workday_zip)
workday_dict = dict(workday_list)

hour_str = ('night','night','night','night','night','night','morning','morning','morning','morning','morning','midday','midday','midday','afternoon','afternoon','evening','evening','evening','evening','night','night','night','night')
hour_num = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23)
hour_zip = zip(hour_num,hour_str)
hour_list= list(hour_zip)
hour_dict = dict(hour_list)

df1['day_name'].replace(day_dict,inplace=True)
df1['workday'].replace(workday_dict,inplace=True)
df1['workday'] = df1['workday'].astype('category')
df1['time_of_day'].replace(hour_dict,inplace=True)
df1['time_of_day'] = df1['time_of_day'].astype('category')

#%% 
'''boxplot 9am Vs 5pm'''
df_midday = df1.loc[
   #(df1['month']==12)&
   ((df1['hour']==9)|(df1['hour']==18))&
   (df1['minute']==0)&
   ((df1['id']==69))
   ]

sns.set_style('darkgrid')
sns.boxplot(x='hour', y='proportion_filled',data=df_midday,
           hue='name'
           )

plt.ylim(0,100)
#%%
'''boxplot time of day by midweek Vs weekend '''

df_time_of_day = df1.loc[
   ((df1['id']==60))
   ]

sns.set_style('darkgrid')
sns.boxplot(x='time_of_day', y='proportion_filled',
            data=df_time_of_day,
            order=['morning','midday','afternoon','evening','night'],
           hue='workday'
           )

plt.ylim(0,100)
#%% 
'''
relplot showing % of bikes in a each stand over the course of a day
I'm hoping that U shaped graphs will show origin stations that people leave during the day ie. peoples homes
n shaped graphs should show destination stations that people arrive at in the morning and leave from at night 
plotting the workday as the hue we should see changes in the stations only used for commuting
'''
sns.set_style('darkgrid')
sns.relplot(
   x='hour',
   y='proportion_filled',
   kind = 'line',
   data=df1,
   col='id',
   col_wrap=10,
   hue = 'workday'
           )

plt.ylim(0,100)

# %%

'''Bring in map, centered on Dublin city '''
bstreet = (53.35677,-6.26814)
df_coords=df.loc[:, ['STATION ID','NAME', 'LATITUDE', 'LONGITUDE']].drop_duplicates().values  
df2=pd.DataFrame(df_coords, columns=['id','name', 'latitude', 'longitude'])
map = folium.Map(location=bstreet, zoom_start=12)
map
# %%
'''Map the coordinates of each station and label them'''
for i in range(0,len(df2)):
   folium.Marker(
      location=[df2.iloc[i]['latitude'], df2.iloc[i]['longitude']],
      popup=df2.iloc[i]['name'],
   ).add_to(map)
#show map again
map
# %%
