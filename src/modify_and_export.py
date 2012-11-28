'''
Created on Nov 28, 2012

@author: hare
'''

import sqlite3
import argparse


#
# specify the following arguments
# 1. the database
# 2. the sql to modify
# 3. (optionally) whether to create a gtfs zip, defaults to yes
# 4. (optionally) flag to write the changes to a new sqlite database with a particular name, also to serialized gtfs zip
#

parser = argparse.ArgumentParser(description='Batch load sql files for GTFS modification.')
parser.add_argument('-d', metavar='database', dest='database', nargs='1', help='the sqlite database to load')
parser.add_argument('-f', metavar='sqlfile', dest='sqlfile', nargs='1', help='the sql to apply')
parser.add_argument('-z', metavar='exportflag', dest='exportflag', nargs='1', default=True, help='toggle export (default: True)')
parser.add_argument('-c', metavar='cloneflag', dest='cloneflag', nargs='1', default=True, help='toggle cloned output (default: True)')

args = parser.parse_args()
print "database is: " + args.database
print "sqlfile is: " + args.sqlfile
print "exportflag is: " + args.exportflag
print "cloneflag is: " + args.cloneflag



# 
# load in the specified database
# duplicate if necessary
# apply the sql in a verbose manner
# export contents into GTFS structure and zip
# 