#!/usr/bin/python

'''
Created on Nov 28, 2012

@author: hare
'''

from __future__ import with_statement
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from gtfsdb import Database, GTFS
import sqlite3
import argparse
import shutil
import csv
import os
import glob
import utilities

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
# standalone function to create a sqlite database for each affected file
#
def loadToDatabase(writedir, name, gtfsfile) :
    db_type = "sqlite:///"
    suffix = ".sqlite"
    dbpath = writedir + "/" + name + suffix
    dbname = db_type + dbpath
    
    print "storing into database as " + dbname
    
    db = Database(dbname, None, False)
    db.create()
    gtfs = GTFS(gtfsfile)
    gtfs.load(db)

    return dbpath

#
# specify the following arguments
# 1. the database
# 2. the sql to modify
# 3. (optionally) whether to create a gtfs zip, defaults to yes
# 4. (optionally) flag to write the changes to a new sqlite database with a particular name, also to serialized gtfs zip
#

parser = argparse.ArgumentParser(description='Batch load sql files for GTFS modification.')
parser.add_argument('-g', metavar='gtfsfile', dest='gtfsfile', help='the GTFS file that will be modified')
parser.add_argument('-f', metavar='sqlfile', dest='sqlfile', help='the sql to apply')
parser.add_argument('-c', metavar='cloneflag', dest='cloneflag', default=True, help='toggle cloned output (default: True)')
parser.add_argument('-z', metavar='exportflag', dest='exportflag', default=True, help='toggle export (default: True)')

args = parser.parse_args()
print "gtfs target file is: " + args.gtfsfile
print "sqlfile is: " + args.sqlfile
print "exportflag is: " + str(args.exportflag)
print "cloneflag is: " + str(args.cloneflag)

# clean name of the file
gtfs_name = args.gtfsfile   
gtfs_shortname = gtfs_name.split("/")[-1].split(".")[0]
gtfs_basename = gtfs_name.split(".")[0]
gtfs_dir = os.path.dirname(gtfs_name)

print "directory is: " + gtfs_dir

dir_fileset = glob.glob(gtfs_dir + utilities.all_pattern)
gtfs_dbstring = gtfs_basename + ".sqlite"

if any(gtfs_dbstring in f for f in dir_fileset) :
    print "sqlite database found; will be deleted NOW" + utilities.newline
    os.remove(gtfs_dbstring)

print "creating sqlite database" + utilities.newline
database_path = loadToDatabase(gtfs_dir, gtfs_shortname, gtfs_name)
    
print "db path is: " + database_path

db_full_name = database_path.split("/")[-1]
db_short_name = db_full_name.split(".")[0]
db_directory = gtfs_dir
db_modify_directory = gtfs_dir + "_modify"

working_db = args.gtfsfile

#
# clone if necessary
#
if (args.cloneflag == True) :
    print "cloning from " + db_directory + " to " + db_modify_directory + utilities.newline
    shutil.copytree(db_directory, db_modify_directory)
    
    db_orig = db_modify_directory + "/" + db_full_name   
    db_clone = db_modify_directory + "/" + db_full_name + "_clone" 
    
    shutil.copy(db_orig, db_clone)
    working_db = db_clone

# 
# using the target database, apply the sql
#
s3_conn = sqlite3.connect(working_db)
sqlfile = open(args.sqlfile, 'r').read()
sc = s3_conn.cursor()
print "applying sql from " + args.sqlfile + utilities.newline
sc.executescript(sqlfile)
s3_conn.commit()
sc.close()

#
# export if necessary
#
if (args.exportflag == True) :

    db_modify_to_delete = db_modify_directory + "/" + db_short_name + ".zip"    
    storedir = db_modify_directory + "/" + db_short_name
    
    os.remove(db_modify_to_delete)
    os.mkdir(storedir)

    print "storing into " + storedir + utilities.newline

    dc = s3_conn.cursor()
    dc.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [x[0] for x in dc.fetchall()]

    for table in tables :
        dc.execute("select * from " + table + ";")
        csv_name = storedir + "/" + table + ".txt"
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
s3_conn.close()
