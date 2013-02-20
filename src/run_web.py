#!/usr/bin/python

'''
Created on 19 Feb, 2013

@author: hare
'''

from boto.ec2.connection import EC2Connection
import argparse
import utilities

ami_id = "ami-809003e9"
output_images_bucket = "output_images"

parser = argparse.ArgumentParser(description='specify a directory of GTFS/graph already uploaded to S3.')
parser.add_argument('-dir', metavar='directory_1', dest='directory_1', help='the first directory to load')

args = parser.parse_args()

dir1 = utilities.trimSlash(args.directory_1)
dir1_bucket = ""

if "/" not in dir1 :
    dir1_bucket = dir1
else :
    dir1_bucket = utilities.getBucketName(dir1)
    
user_string = ""
user_string += utilities.base_string
user_string += utilities.setAwsPerms()
user_string += utilities.pullFromS3(dir1_bucket, ["Graph.obj"], useOriginalFiles=True)
#user_string += utilities.generateAnalystImage(dir1_bucket, date, time, searchCutOff, thresholdAccum, thresholdAgg, maxWalkDist, origin, tiffname)
user_string += utilities.writeAnalystImageToS3(output_images_bucket)
user_string += utilities.emailLogAndQuit()

ec2_conn = EC2Connection()

utilities.spawnAwsInstance(ec2_conn, ami_id, user_string)