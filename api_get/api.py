import json
import urllib.request
import pprint
import pandas as pd

with open('./api_key.json') as f:
    api_key_sample = json.load(f)

with open('./api_key.json') as f:
    api_key = json.load(f)

apiEndPoint = 'https://opendata.resas-portal.go.jp/'

with open('./cityJson.json') as f:
    cityData = json.load(f)

i = 0
for citydata in cityData['result']:
    urlPopulation = apiEndPoint + "api/v1/population/sum/estimate?prefCode=13&cityCode=" + citydata['cityCode']
    req = urllib.request.Request(urlPopulation, headers=api_key)
    with urllib.request.urlopen(req) as response:
        Municipality = response.read()
    cityJsonAddMunicipality = json.loads(Municipality)
    if not cityJsonAddMunicipality['result'] is None:
        cityData['result'][i].update(cityJsonAddMunicipality['result']['data'][0]['data'][-1])
        i+=1

# print(cityData)
with open("cityData.json", 'w') as outfile:
    json.dump(cityData, outfile, indent=4, ensure_ascii=False)

# pprint.pprint(cityJsonAddMunicipality)
# twentyLater = ""
