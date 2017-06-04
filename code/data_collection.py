#!/home/bks4line/anaconda2/bin/python
# Author : Karthik Balasubramanian

import json
import urllib
from urlparse import urlparse
import httplib2 as http #External library
import pandas as pd
import time
from datetime import datetime
from pytz import timezone
import os

headers = { 'AccountKey' : 'J4mwYTb4FKiNkWpDHLapZQ==','accept' : 'application/json'}

uri = 'http://datamall2.mytransport.sg/' #Resource URL
path = 'ltaodataservice/Taxi-Availability?$skip='
fmt =  '%Y-%m-%d_%H:%M:%S'
sg = timezone('Asia/Singapore')
dir_path = os.path.dirname(os.path.realpath(__file__))+"/data"



def get_data_from_LDA(filename):
	
	global headers,uri,path,fmt,sg,dir_path

	
 	#Build query string & specify type of API call
 	
 	final_list = []
 	target = urlparse(uri + path+str(len(final_list)))

	
	
 	method = 'GET'
 	body = ''

	#Get handle to http
	h = http.Http()
	
	# Obtain results
	response, content = h.request(target.geturl(),method,body,headers)

	# Parse JSON to print
	jsonObj = json.loads(content)
	
	final_list.extend(jsonObj["value"])
	
	while(len(jsonObj["value"])>0):
		target = urlparse(uri + path+str(len(final_list)))
	 	# print target.geturl()
	 	response, content = h.request(target.geturl(),method,body,headers)
	 	jsonObj = json.loads(content)
	 	final_list.extend(jsonObj["value"])
	# print
	
	time_now_in_sg = datetime.now(sg)
	date_and_time_ff =  time_now_in_sg.strftime(fmt)
	date_and_time = date_and_time_ff.split("_")
	date_in_sg = [date_and_time[0]]*len(final_list)
	time_in_sg =  [date_and_time[1]]*len(final_list)
	
	df = pd.DataFrame(final_list)
	df['date'] = pd.Series(date_in_sg, index=df.index)
	df['time'] = pd.Series(time_in_sg, index=df.index)
	# print df.head()
	if not filename:
		filename =  dir_path+"/taxi_"+date_and_time_ff+".csv"
		df.to_csv(filename)
	else:
		file_size_exceed = float(os.path.getsize(filename))/float(5e+6)
		if file_size_exceed>1.0:
			print "file_size_exceed"
			filename = dir_path+"/taxi_"+date_and_time_ff+".csv"
			print "new file name {0}".format(filename)
			df.to_csv(filename)
		else:
			print "file size not exceeded"
			df.to_csv(filename, mode='a', header=False)

	return filename



if __name__=="__main__":	

 
 	starttime =  time.time()
 	filename = None
 	# get_data_from_LDA(filename=None)
 	while True:
 		filename = get_data_from_LDA(filename)
 		starttime =  time.mktime(datetime.now().timetuple())
 		time.sleep(50.0 - ((time.time() - starttime) % 60.0))

