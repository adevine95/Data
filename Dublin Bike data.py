#%%
import pandas as pd
import folium
#%%

df = pd.read_csv('dublinbikes_20211001_20220101.csv')
# %%
bstreet = (53.35677,-6.26814)

df_coords=df.loc[:, ['NAME', 'LATITUDE', 'LONGITUDE']].drop_duplicates().values  
df2=pd.DataFrame(df_coords, columns=['Name', 'Latitude', 'Longitude'])
#%%

map = folium.Map(location=bstreet, zoom_start=12)
map
# %%
for i in range(0,len(df2)):
   folium.Marker(
      location=[df2.iloc[i]['Latitude'], df2.iloc[i]['Longitude']],
      popup=df2.iloc[i]['Name'],
   ).add_to(map)
    

# %%
map
# %%
