

import geopandas as gpd 
import pandas as pd
from shapely.geometry import *
import glob


def create_geometry(df):
    geometry_arr = df.apply(lambda x: Point(x['X'], x['Y']), axis=1)
    df = df.assign(geometry=geometry_arr)
    gdf = gpd.GeoDataFrame(df)
    return gdf


def filter_points(pts_gpd, poly):
    index = pts_gpd.apply(lambda x: not poly.contains(x['geometry']), axis=1)
    return pts_gpd.loc[index]



def main():
	# likewise for bus as well 
	# /home/hchin/LTA/Analysis/bus_data/bus_report*.csv

	file_list = glob.glob("/home/hchin/LTA/Analysis/taxi_data/taxi_report_*.csv")
	airport = gpd.GeoDataFrame.from_file('airport.shp')
	for each_file in file_list:
		gdf = pd.read_csv(each_file)
		new_df = create_geometry(gdf)
		new_df_without_a_p = filter_points(new_df, airport['geometry'].iloc[0])
		new_df_without_a_p.to_file(filename+'_filter.shp', driver='ESRI Shapefile')



if __name__ == '__main__':
	main()