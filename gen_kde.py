import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

import multiprocessing as mp
import scipy.misc

import glob

class SG_kde():

	def __init__(self, fn):
		self.sample_loc = np.genfromtxt(fn, delimiter=',', dtype=np.int)
		self.scale = 100
		minv = np.min(self.sample_loc,axis=0)
		maxv = np.max(self.sample_loc,axis=0)
		self.bounds = np.array([minv[0], minv[1], maxv[0], maxv[1]])
		self.nX = int( (maxv[0]-minv[0])/self.scale+1)
		self.nY = int( (maxv[1]-minv[1])/self.scale+1)

	def create_kde(self, data):
		self.kde = KernelDensity(bandwidth=1000, metric='minkowski',
							kernel='epanechnikov', algorithm='kd_tree')
		self.kde.fit(data)

	def generate_map(self):
		im = np.zeros( (self.nY, self.nX), dtype=np.float)
		Z = np.exp(self.kde.score_samples(self.sample_loc))																																																																																
		Z = np.clip(Z,0,1)
		dx = self.bounds[0]
		dy = self.bounds[1]
		for i, z in enumerate(Z):
			x = int((self.sample_loc[i][0]-dx)/self.scale)
			y = self.nY-int((self.sample_loc[i][1]-dy)/self.scale)-1
			im[y,x] = z
		return im


def process_bus(fn, tn, kde_gen):
	df = pd.read_csv(fn)
	df['time'] = pd.to_datetime(df['time'])
	df.set_index('time', inplace=True)
	grouped = df.groupby(pd.TimeGrouper(freq='15Min'))
	count = 0
	for i, g in grouped:
		dt = i.to_pydatetime()
		if len(g) == 0:
			continue
		fn_out = './kde/{}_{}_{:02d}{:02d}.jpg'.format(tn,dt.day,dt.hour,dt.minute)
		kde_gen.create_kde(g[['X','Y']].values)
		kde_im = kde_gen.generate_map()
		scipy.misc.imsave(fn_out, kde_im)
		print(fn_out)
		
def process_taxi(fn, tn, kde_gen):

	df = pd.read_csv(fn)
	df['datetime'] = pd.to_datetime(df['date']+' '+df['time'])
	df.set_index('datetime', inplace=True)
	grouped = df.groupby(pd.TimeGrouper(freq='15Min'))
	count = 0
	for i, g in grouped:
		dt = i.to_pydatetime()
		if len(g) == 0:
			continue
		fn_out = './kde/{}_{}_{:02d}{:02d}.jpg'.format(tn,dt.day,dt.hour,dt.minute)
		kde_gen.create_kde(g[['X','Y']].values)
		kde_im = kde_gen.generate_map()
		scipy.misc.imsave(fn_out, kde_im)
		
		

if __name__ == '__main__':

	SG = SG_kde('sg_utm_coords.txt')

	file_list = glob.glob("../data/bus_data/bus_report_*.csv")
	for fn in file_list:
		process_bus(fn, 'bus', SG)

	file_list = glob.glob("../data/taxi_data/taxi_report_14_no_airport.csv")
	for fn in file_list:
		print(fn)
		process_taxi(fn, 'taxi', SG)
		
	
	
	#SG.create_kde(df[['X','Y']].values)	

	#kde_im = SG.generate_map()
	#scipy.misc.imsave('outfile.png', kde_im)

