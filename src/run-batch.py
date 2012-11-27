'''
Created on Nov 20, 2012

@author: hare
'''

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from gtfsdb import Database, GTFS
import sys

import sqlite3
import zipfile


_AWS_ACCESS_KEY = "AKIAJ4YM7LJUTBFMED6A"
_AWS_SECRET_KEY = "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"

base_path = "/otp/cache/nyc-hacked/"
modify_path = "/otp/cache/nyc-hacked/"

sqliteSuffix = ".sqlite"

db_type = "sqlite:////otp/cache/nyc-hacked/"

testFile = "/otp/cache/nyc-hacked/queens.zip"
testOut = "queens"

dbname = db_type + testOut + sqliteSuffix

print "db is " + dbname + "\n"
print "about to try out the run for " + testFile + "\n"

#db = Database(dbname, None, False)
#db.create()
#print "serialized db is " + db.__str__() + "\n"
#
#gtfs = GTFS(testFile)
#gtfs.load(db)


'''
dump GTFS databases to files and send over 
'''


'''
you will need to use the sqlite python bindings to run the equivalent of the following:
[ hare@interval:nyc-hacked ] $ sqlite3 queens.sqlite <<!
> .headers on
> .mode csv
> .output qns_stop.csv
> select * from stop_times;
> !

and then use the zipfile commands to reconstruct the zips as required for dispatch

'''



'''
dispatch unchanged GTFS files to S3
'''

conn = S3Connection(_AWS_ACCESS_KEY, _AWS_SECRET_KEY)
bucket = conn.create_bucket("test_bucket_otp_analyst")  

bronx = Key(bucket)
brooklyn = Key(bucket)
manhattan = Key(bucket)
queens = Key(bucket)
staten = Key(bucket)
busco = Key(bucket)
lirr = Key(bucket)
mnrr = Key(bucket)
subway = Key(bucket)


bronx.key = "bronx_base"
bronx.set_contents_from_filename(base_path + "bronx.zip")

brooklyn.key = "brooklyn_base"
brooklyn.set_contents_from_filename(base_path + "brooklyn.zip")

manhattan.key = "manhattan_base"
manhattan.set_contents_from_filename(base_path + "manhattan.zip")

queens.key = "queens_base"
queens.set_contents_from_filename(base_path + "queens.zip")

staten.key = "staten_base"
staten.set_contents_from_filename(base_path + "staten.zip")

busco.key = "busco_base"
busco.set_contents_from_filename(base_path + "busco.zip")

lirr.key = "lirr_base"
lirr.set_contents_from_filename(base_path + "lirr.zip")

mnrr.key = "mnrr_base"
mnrr.set_contents_from_filename(base_path + "mnrr.zip")

subway.key = "subway_base"
subway.set_contents_from_filename(base_path + "subway.zip")



'''
dispatch **modified** GTFS files to S3
'''

bronx.key = "bronx_modify"
bronx.set_contents_from_filename(modify_path + "bronx.zip")

brooklyn.key = "brooklyn_modify"
brooklyn.set_contents_from_filename(modify_path + "brooklyn.zip")

manhattan.key = "manhattan_modify"
manhattan.set_contents_from_filename(modify_path + "manhattan.zip")

queens.key = "queens_modify"
queens.set_contents_from_filename(modify_path + "queens.zip")

staten.key = "staten_modify"
staten.set_contents_from_filename(modify_path + "staten.zip")

busco.key = "busco_modify"
busco.set_contents_from_filename(modify_path + "busco.zip")

lirr.key = "lirr_modify"
lirr.set_contents_from_filename(modify_path + "lirr.zip")

mnrr.key = "mnrr_modify"
mnrr.set_contents_from_filename(modify_path + "mnrr.zip")

subway.key = "subway_modify"
subway.set_contents_from_filename(modify_path + "subway.zip")



'''
dispatch OSM file to S3
'''

osm = Key(bucket)
osm.key = "osm"
osm.set_contents_from_filename(base_path + "nyc-osm.pbf")

'''
generate base graph and store to S3 (via AWS)
'''


'''
generate modified graph and store to S3 (via AWS)
'''


'''
passing in a single config, run batch analysis on base graph
generate TIFF and write to S3
'''

'''
passing in a single config, run batch analysis on modified graph
generate TIFF and write to S3
'''

'''
send email that the TIFFs are done 
'''

'''
using local script, copy tiffs over, and run QGIS
'''

base_tiff = Key(bucket)
modified_tiff = Key(bucket)

'''
TODO: figure out exactly where these will be stored
'''
base_tiff.get_contents_to_filename("base.tiff")
modified_tiff.get_contents_to_filename("modified.tiff")




