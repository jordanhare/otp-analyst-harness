'''
Created on Nov 27, 2012

@author: hare
'''

import requests
from gtfsdb import Database, GTFS
import sys

import sqlite3
import zipfile

feeds = []

'''
Define data structures for each GTFS feed
'''

subway = {"url" : "http://mta.info/developers/data/nyct/subway/google_transit.zip",
          "name" : "subway",
          "file" : "subway_gtfs.zip" }
feeds.append(subway)

bronx = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_bronx.zip",
          "name" : "bronx",
          "file" : "bronx_bus_gtfs.zip" }
feeds.append(bronx)

brooklyn = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_brooklyn.zip",
          "name" : "brooklyn",
          "file" : "brooklyn_bus_gtfs.zip" }
feeds.append(brooklyn)

manhattan = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_manhattan.zip",
          "name" : "manhattan",
          "file" : "manhattan_bus_gtfs.zip" }
feeds.append(manhattan)

queens = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_queens.zip",
          "name" : "queens",
          "file" : "queens_bus_gtfs.zip" }
feeds.append(queens)

staten_island = {"url" : "http://mta.info/developers/data/nyct/bus/google_transit_staten_island.zip",
          "name" : "staten_island",
          "file" : "staten_island_bus_gtfs.zip" }
feeds.append(staten_island)

busco = {"url" : "http://mta.info/developers/data/busco/google_transit.zip",
          "name" : "busco",
          "file" : "busco_gtfs.zip" }
feeds.append(busco)

lirr = {"url" : "http://mta.info/developers/data/lirr/google_transit.zip",
          "name" : "lirr",
          "file" : "lirr_gtfs.zip", 
          "sqlite" : True}
feeds.append(lirr)

mnr = {"url" : "http://mta.info/developers/data/mnr/google_transit.zip",
          "name" : "mnr",
          "file" : "mnr_gtfs.zip" }
feeds.append(mnr)

'''
Write each GTFS feed to a file
if specified above, write to a sql database
'''

for feed in feeds:
    print "downloading file for " + feed["name"] + "\n"
    r = requests.get(feed["url"])
    with open(feed["file"], "wb") as code:
        code.write(r.content)
    if (feed["sqlite"] == True):
        print "writing to database"


'''
standalone function to create a sqlite database for each affected file
'''

def loadToDatabase(name) :
    dbname = "foo" 
    testFile = "bar"
    db = Database(dbname, None, False)
    db.create()
    
    gtfs = GTFS(testFile)
    gtfs.load(db)
    
    return db



