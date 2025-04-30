import logging
from datetime import datetime
import os
os.makedirs('log', exist_ok=True)
logging.basicConfig(filename=f'log/listFacilitiesInArea{datetime.now().strftime("%m%d%H%M")}.log', filemode='w', level=logging.DEBUG, format='%(asctime)s-%(levelname)s: %(message)s')

import urllib.parse
import urllib.request
import json

# allAmenities='''
# [out:json];
# node['amenity']['addr:city'='札幌市'];
# out body;
# '''
# allAmenitiesWay='''
# [out:json];
# way['amenity']['addr:city'='札幌市'];
# out body;
# '''
# allAmenitiesWay='''
# [out:json];
# way['amenity']['addr:city'='札幌市'];
# out body;
# '''

queryTags=['amenity','leisure','shop','tourism','historic']
dataTypes=['node','way']

def constructOSMQL(queryTag:str, dataType:str, city:str):
    """
    construct the OSMQL query string
    """
    query = '[out:json];'
    query += f'{dataType}[\'{queryTag}\'][\'addr:city\'=\'{city}\'];'
    if dataType == 'way':
        query += 'out geom;'
    else:
        query += 'out body;'
    return query

def queryOSM(OSMQL:str, OUTPUT_PATH:str):
    url = 'https://z.overpass-api.de/api/interpreter?data='
    e = urllib.parse.quote(OSMQL)
    url += e
    with urllib.request.urlopen(url) as r:
        response = r.read() # type:bytes

    resjson = json.loads(response)
    with open(OUTPUT_PATH, 'w',encoding='utf-8') as fp:
        json.dump(resjson, fp, indent=4, ensure_ascii=False)

    # elements = resjson['elements']
    # osmList = list()
    # for element in elements:
    #     name = element['tags']['name:ja']
    #     coordinates = (element['lat'], element['lon'])
    #     osmList.append(name + '\t' + str(coordinates)+'\n')
    # return osmList

def extractJANames(QUERY_RESULT_PATH:str):
    ## doesnt work for way yet...
    with open(QUERY_RESULT_PATH, 'r',encoding='utf-8') as fp:
        resjson = json.load(fp)
    elements = resjson['elements']
    osmList = list()
    for element in elements:
        if 'name:ja' in element['tags']:
            name = element['tags']['name:ja']
        elif 'name' in element['tags']:
            print('no ja name')
            name = element['tags']['name']
        else:
            print('no name',element)
            pass
        
        if 'branch' in element['tags']: name += element['tags']['branch']
        coordinates = (element['lat'], element['lon'])
        osmList.append(f'{name}\t{str(coordinates)}')
    return osmList

for dataType in dataTypes:
    for queryTag in queryTags:
        queryFacilitiesSapporo = constructOSMQL(queryTag, dataType, '札幌市')
        queryOSM(queryFacilitiesSapporo, f'./response_{queryTag}_{dataType}.json')
        with open(f'./output_{queryTag}_{dataType}.txt', 'w',encoding='utf-8') as f:
            f.writelines('\n'.join(extractJANames(f'./response_{queryTag}_{dataType}.json')))
