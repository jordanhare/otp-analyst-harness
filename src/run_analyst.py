#!/usr/bin/python

'''
Created on Dec 5, 2012

@author: hare
'''

from boto.ec2.connection import EC2Connection
import argparse
import utilities

ami_id = "ami-809003e9"
output_images_bucket = "output_images"

parser = argparse.ArgumentParser(description='specify a directory of GTFS/graph already uploaded to S3.')
parser.add_argument('-dir', metavar='directory_1', dest='directory_1', help='the first directory to load')
parser.add_argument('-date', metavar='date', dest='date', help='the date')
parser.add_argument('-time', metavar='time', dest='time', help='the time')
parser.add_argument('-origin', metavar='origin', dest='origin', help='origin file')
parser.add_argument('-tiffname', metavar='tiffname', dest='tiffname', help='name of tiff file')

args = parser.parse_args()

dir1 = utilities.trimSlash(args.directory_1)
dir1_bucket = ""

date = args.date
time = args.time
origin = args.origin
tiffname = args.tiffname

# keep these as defaults for now
searchCutOff = "2400"
thresholdAccum = "2400"
thresholdAgg="2400"
maxWalkDist="700"

if "/" not in dir1 :
    dir1_bucket = dir1
else :
    dir1_bucket = utilities.getBucketName(dir1)
    
user_string = ""
user_string += utilities.base_string
user_string += utilities.setAwsPerms()
user_string += utilities.pullFromS3(dir1_bucket, ["Graph.obj"], useOriginalFiles=True)
user_string += utilities.generateAnalystImage(dir1_bucket, date, time, searchCutOff, thresholdAccum, thresholdAgg, maxWalkDist, origin, tiffname)
user_string += utilities.writeAnalystImageToS3(dir1_bucket, tiffname)
user_string += utilities.emailLogAndQuit()


ec2_conn = EC2Connection()

utilities.spawnAwsInstance(ec2_conn, ami_id, user_string)