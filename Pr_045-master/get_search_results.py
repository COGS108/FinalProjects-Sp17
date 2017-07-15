#!/usr/bin/env python

import zillow
import pprint
import random
import json

if __name__=="__main__":
    key = "X1-ZWz196b0emyd57_8p8sy"

    f = open('houseData4.json', 'w')
    minL = 16817995 
    maxL = 16834401
    list = []
    for x in range(100):
        r = random.randint(minL,maxL)
        list.append(r)

    for y in range(100):
        api = zillow.ValuationApi()

        detail_data = api.GetZEstimate(key, list[y])
        f.write(json.dumps(detail_data.get_dict()))
        pp = pprint.PrettyPrinter(indent=4)
        #address = "13147 Trail Dust Ave. San Diego, CA"
        #postal_code = "92129"

        #data = api.GetSearchResults(key, address, postal_code)

        #pp.pprint(data.get_dict())


       # comp_data = api.GetComps(key, data.zpid)

       
       # pp.pprint(comp_data['comps'][1].get_dict())
       # pp.pprint("______________________________")


    #locData = api.GetRegionChildren(key)
    #pp.pprint(locData.get_dict())

    #deep_results = api.GetDeepSearchResults(key, "1920 1st Street South Apt 407, Minneapolis, MN", "55454")
    #pp.pprint(deep_results.get_dict())