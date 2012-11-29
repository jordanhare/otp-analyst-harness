#!/usr/bin/python

'''
Created on Nov 27, 2012

@author: hare
'''

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import argparse
import glob

def trimSlash(dirname) :
    if (dirname[-1:] == "/") :
        return dirname.rstrip("/")
    else :
        return dirname

def uploadToS3(dirname, conn) :
    file_set = glob.glob(dirname + match_pattern)
    bucket_name = dirname.split("/")[-1]
    bucket = conn.create_bucket(bucket_name)
    print "dirname " + dirname + " stored into bucket " + bucket_name 
    for file_entry in file_set :
        file_short = file_entry.split("/")[-1].split(".")[0]
        key = Key(bucket)
        key.key = file_short
        print "storing as key: " + file_short
        key.set_contents_from_filename(file_entry)        

_AWS_ACCESS_KEY = "AKIAJ4YM7LJUTBFMED6A"
_AWS_SECRET_KEY = "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"
match_pattern = "/*.zip"

parser = argparse.ArgumentParser(description='specify two directories of GTFS. for each directory, uploaded to S3, create graph.')
parser.add_argument('-dir1', metavar='directory_1', dest='directory_1', help='the first directory to load')
parser.add_argument('-dir2', metavar='directory_2', dest='directory_2', help='the second directory to load')

args = parser.parse_args()

dir1 = trimSlash(args.directory_1)
dir2 = trimSlash(args.directory_2)

#
# establish connection to S3
#
conn = S3Connection(_AWS_ACCESS_KEY, _AWS_SECRET_KEY)

#
# upload files to S3
#
uploadToS3(dir1, conn)
uploadToS3(dir2, conn)

