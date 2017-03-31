import requests

if __name__=="__main__":
	#Authentication parameters
 	headers = { 'AccountKey' : 'J4mwYTb4FKiNkWpDHLapZQ==',
 	'accept' : 'application/json'} #this is by default

 	#API parameters
 	uri = 'http://datamall2.mytransport.sg/' #Resource URL
 	path = 'ltaodataservice/Taxi-Availability?'
 	#Build query string & specify type of API call
 	target_url = uri + path
 	res = requests.get(target_url headers = headers)
 	print(res.status_code)
 	print(res.json())
