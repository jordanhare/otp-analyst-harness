#!/usr/bin/python

'''
Created on Nov 27, 2012

@author: hare
'''

from boto.s3.connection import S3Connection
from boto.ec2.connection import EC2Connection

import argparse
import utilities
import glob

ami_id = "ami-809003e9"

parser = argparse.ArgumentParser(description='specify two directories of GTFS. for each directory, uploaded to S3, create graph.')
parser.add_argument('-dir', metavar='directory_1', dest='directory_1', help='the first directory to load')

args = parser.parse_args()

dir1 = utilities.trimSlash(args.directory_1)

dir1_bucket = utilities.getBucketName(dir1)
dir1_fileset = glob.glob(dir1 + utilities.zip_pattern)

# upload files to S3
#
s3_conn = S3Connection()
utilities.uploadToS3(dir1_bucket, dir1_fileset, s3_conn)

# dynamically construct user data script 
#
user_string = "" 
user_string += utilities.base_string 
user_string += utilities.setAwsPerms()
user_string += utilities.pullFromS3(dir1_bucket, dir1_fileset)#user_string += utilities.pullFromS3(dir2_bucket, dir2_fileset)

user_string += utilities.generateGraph(dir1_bucket)
user_string += utilities.writeGraphToS3(dir1_bucket)

user_string += utilities.emailLogAndQuit()

#
# start up instance
# pull down S3 data into filesystem
# run graph builder
# post graph object into s3
# shutdown instance
#

ec2_conn = EC2Connection()

utilities.spawnAwsInstance(ec2_conn, ami_id, user_string)

