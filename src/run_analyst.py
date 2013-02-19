#!/usr/bin/python

'''
Created on Dec 5, 2012

@author: hare
'''

from boto.ec2.connection import EC2Connection

import argparse
#import sys
#import os
import utilities

ami_id = "ami-4ef16127"
output_images_bucket = "output_images"

parser = argparse.ArgumentParser(description='specify two directories of GTFS. for each directory, uploaded to S3, create graph.')
parser.add_argument('-dir', metavar='directory_1', dest='directory_1', help='the first directory to load')
#parser.add_argument('-dir2', metavar='directory_2', dest='directory_2', help='the second directory to load')
parser.add_argument('-date', metavar='date', dest='date', help='the date')
parser.add_argument('-time', metavar='time', dest='time', help='the time')
parser.add_argument('-origin', metavar='origin', dest='origin', help='origin file')
parser.add_argument('-tiffname', metavar='tiffname', dest='tiffname', help='name of tiff file')

args = parser.parse_args()

dir1 = utilities.trimSlash(args.directory_1)
#dir2 = utilities.trimSlash(args.directory_2)

dir1_bucket = ""
dir2_bucket = ""

if "/" not in dir1 :
    dir1_bucket = dir1
#    dir2_bucket = dir2
else :
    dir1_bucket = utilities.getBucketName(dir1)
#    dir2_bucket = utilities.getBucketName(dir2)
    
user_string = ""
user_string += utilities.base_string
user_string += utilities.setAwsPerms()

user_string += utilities.pullFromS3(dir1_bucket, ["Graph.obj"], useOriginalFiles=True)

date = args.date
time = args.time
origin = args.origin
tiffname = args.tiffname

#date = "2013-02-10"
#time = "15:00"

# keep these as defaults for now
searchCutOff = "2400"
thresholdAccum = "2400"
thresholdAgg="2400"
maxWalkDist="700"


user_string += utilities.generateAnalystImage(dir1_bucket, date, time, searchCutOff, thresholdAccum, thresholdAgg, maxWalkDist, origin, tiffname)
user_string += utilities.writeAnalystImageToS3(output_images_bucket)
user_string += utilities.emailLogAndQuit()


ec2_conn = EC2Connection()

utilities.spawnAwsInstance(ec2_conn, ami_id, user_string)