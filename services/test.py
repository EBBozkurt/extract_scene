import json


with open('control2.json','w') as jfile:
    data = {"control":0}
    json.dump(data,jfile) 