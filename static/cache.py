import requests
import json
import time

headers = {
    'AccountKey': 'J4mwYTb4FKiNkWpDHLapZQ==',
    'accept': 'application/json'
}

def fetch_all(url):
    results = []
    while True:
        new_results = requests.get(
            url,
            headers=headers,
            params={'$skip': len(results)}
        ).json()['value']
        if new_results == []:
            break
        else:
            results += new_results
    return results

if __name__ == "__main__":
    today = time.strftime("%d%m%y")
    print("fetching data from lta datamall @ "+today)

    stops = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusStops")
    with open("stops_"+today+".json", "w") as f:
        f.write(json.dumps(stops))
    print("collected bus stops")
    
    services = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusServices")
    
    with open("services_"+today+".json", "w") as f:
        f.write(json.dumps(services))
    print("collected bus services")

    routes = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusRoutes")
    
    with open("routes_"+today+".json", "w") as f:
        f.write(json.dumps(routes))
    print("collected bus routes")