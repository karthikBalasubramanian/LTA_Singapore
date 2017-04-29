import pandas as pd
import geopandas as gp
import numpy as np
import pyproj as pp
import multiprocessing as mp
import glob

from shapely.geometry import Point


def project(lat, lon):
	x,y = pp.transform(pp.Proj(init='EPSG:4326'), pp.Proj(init='EPSG:32648'), lon,lat)
	return (x,y)

def main():
	file_list = glob.glob("../data/taxi_data/taxi_report_*.csv")
	pool = mp.Pool(processes=8)
	for file in file_list:
		df = pd.read_csv(file)
		fn = file.split('/')
		new_fn = '/'.join(fn[:-1])+'/utm/'+fn[-1]
		print(new_fn)
		lat = df['Latitude'].values
		lon = df['Longitude'].values
		X,Y = zip(*pool.starmap(project, zip(lat, lon))) 
		D = {'X':X, 'Y':Y, 'date':df['date'].values, 'time':df['time'].values}
		new_df = pd.DataFrame.from_dict(D)
		new_df.to_csv(new_fn, index= False)
		
	pool.close()

if __name__ == '__main__':
	main()