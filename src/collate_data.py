#!/usr/bin/python

'''
Created on Nov 27, 2012

@author: hare
'''

import requests
import datetime
import os

#
# Define data structures for each GTFS feed
#
def setupData(feeds):

    subway = {"url" : "http://mta.info/developers/data/nyct/subway/google_transit.zip",
              "name" : "subway",
              "file" : "subway.zip" }
    feeds.append(subway)
    
    bronx = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_bronx.zip",
             "name" : "bronx",
             "file" : "bronx_bus.zip" }
    feeds.append(bronx)
    
    brooklyn = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_brooklyn.zip",
                "name" : "brooklyn",
                "file" : "brooklyn_bus.zip" }
    feeds.append(brooklyn)
    
    manhattan = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_manhattan.zip",
                 "name" : "manhattan",
                 "file" : "manhattan_bus.zip" }
    feeds.append(manhattan)
    
    queens = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_queens.zip",
              "name" : "queens",
              "file" : "queens_bus.zip" }
    feeds.append(queens)
    
    staten_island = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_staten_island.zip",
                     "name" : "staten_island",
                     "file" : "staten_island_bus.zip" }
    feeds.append(staten_island)

    busco = {"url" : "http://mta.info/developers/data/busco/google_transit.zip",
             "name" : "busco",
             "file" : "busco.zip" }
    feeds.append(busco)
    
    lirr = {"url" : "http://mta.info/developers/data/lirr/google_transit.zip",
            "name" : "lirr",
            "file" : "lirr.zip" }
    feeds.append(lirr)
    
    mnr = {"url" : "http://mta.info/developers/data/mnr/google_transit.zip",
           "name" : "mnr",
           "file" : "mnr.zip" }
    feeds.append(mnr)


#
# Write each GTFS feed to a file, in a directory based on current datetime
#
nowdir = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "/"
basedir = "/Users/hare/projects/otp-data/"
writedir = basedir + nowdir

os.mkdir(writedir)
feeds = []
setupData(feeds)

for feed in feeds:
    filename = writedir + feed["file"]
    print "downloading file for " + feed["name"] + " and storing as " + filename
    r = requests.get(feed["url"])
    with open(filename, "wb") as code:
        code.write(r.content)
