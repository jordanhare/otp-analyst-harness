#!/usr/bin/python

'''
Created on Nov 28, 2012

@author: hare
'''

from __future__ import with_statement
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import sqlite3
import argparse
import shutil
import csv
import os

#
# subroutine to zip up files back into GTFS easily
# see http://stackoverflow.com/questions/296499/how-do-i-zip-the-contents-of-a-folder-using-python-version-2-5
#
def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)


#
# specify the following arguments
# 1. the database
# 2. the sql to modify
# 3. (optionally) whether to create a gtfs zip, defaults to yes
# 4. (optionally) flag to write the changes to a new sqlite database with a particular name, also to serialized gtfs zip
#

parser = argparse.ArgumentParser(description='Batch load sql files for GTFS modification.')
parser.add_argument('-d', metavar='database', dest='database', help='the sqlite database to load (path rel to loc)')
parser.add_argument('-f', metavar='sqlfile', dest='sqlfile', help='the sql to apply')
parser.add_argument('-c', metavar='cloneflag', dest='cloneflag', default=True, help='toggle cloned output (default: True)')
parser.add_argument('-z', metavar='exportflag', dest='exportflag', default=True, help='toggle export (default: True)')

args = parser.parse_args()
print "database is: " + args.database
print "sqlfile is: " + args.sqlfile
print "exportflag is: " + str(args.exportflag)
print "cloneflag is: " + str(args.cloneflag)

db_full_name = args.database.split("/")[-1]
db_short_name = db_full_name.split(".")[0]

db_directory = args.database.replace(args.database.split("/")[-1], "").rstrip("/")
db_modify_directory = db_directory + "_modify" 

working_db = args.database

#
# clone if necessary
#
if (args.cloneflag == True) :
    shutil.copytree(db_directory, db_modify_directory)
    
    db_orig = db_modify_directory + "/" + db_full_name   
    db_clone = db_modify_directory + "/" + db_full_name + "_clone" 
    
    shutil.copy(db_orig, db_clone)
    working_db = db_clone


# 
# using the target database, apply the sql
#
sql_conn = sqlite3.connect(working_db)
sqlfile = open(args.sqlfile, 'r').read()
sc = sql_conn.cursor()
sc.executescript(sqlfile)
sql_conn.commit()
sc.close()

#
# export if necessary
#
if (args.exportflag == True) :

    db_modify_to_delete = db_modify_directory + "/" + db_short_name + ".zip"    
    storedir = db_modify_directory + "/" + db_short_name
    
    os.remove(db_modify_to_delete)
    os.mkdir(storedir)

    dc = sql_conn.cursor()
    dc.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [x[0] for x in dc.fetchall()]

    for table in tables :
        dc.execute("select * from " + table + ";")
        csv_name = storedir + "/" + table + ".csv"
        csv_writer = csv.writer(open(csv_name, "wt"))
        csv_writer.writerow([i[0] for i in dc.description]) # write headers
        csv_writer.writerows(dc)
        del csv_writer # this will close the CSV file

    dc.close()
    
    zipdir(storedir, storedir + ".zip")
    shutil.rmtree(storedir)
    
#
# program is complete; shut down connection
#
sql_conn.close()
