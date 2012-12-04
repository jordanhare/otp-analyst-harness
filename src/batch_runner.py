#!/usr/bin/python

'''
Created on Nov 27, 2012

@author: hare
'''

from boto.s3.connection import S3Connection
from boto.ec2.connection import EC2Connection
from boto.s3.key import Key

import argparse
import glob
import sys
import os

match_pattern = "/*.zip"
ami_id = "ami-a33ebeca"

base_string = """#cloud-config
 
runcmd:
 - mount /dev/sdf1 /mnt/ebs 
 - export HOME=/home/ec2-user
"""

access_key_str = "AWS_ACCESS_KEY_ID"
secret_key_str = "AWS_SECRET_ACCESS_KEY"

newline = "\n"
homedir = "/home/ec2-user/"
s3copy_string = " - /usr/bin/java -jar /home/ec2-user/s3cp/s3cp-cmdline-0.1.11.jar "

def trimSlash(dirname) :
    if (dirname[-1:] == "/") :
        return dirname.rstrip("/")
    else :
        return dirname

def getBucketName(dirname) :
    return dirname.split("/")[-1]

def getFileSet (dirname) :
    return glob.glob(dirname + match_pattern)

def getFileName (longFileName) :
    return longFileName.split("/")[-1].split(".")[0]

def uploadToS3(bucket, file_set, s3_conn) :
    b = s3_conn.create_bucket(bucket)
    b.set_acl('public-read') 
    for f in file_set :
        print "f " + f + " stored into b " + bucket
        f_short = getFileName(f)
        key = Key(b)
        key.key = f_short
        print "storing as key: " + f_short
        key.set_contents_from_filename(f)        
        key.set_acl('public-read')

def pullFromS3(bucket, file_set) :
    return_str = ""
    return_str += " - mkdir /home/ec2-user/" + bucket + newline
    for f in file_set :
        f_short = getFileName(f)        
        return_str += s3copy_string + "s3://" + bucket + "/" + f_short + " " + homedir + bucket + "/" + f_short + ".zip" + newline
    return return_str

def generateGraph(bucket) :
    return_str = ""
    return_str += " - export DIR1=" + bucket + newline
    return_str += " - mkdir -p /mnt/ebs/otp/" + bucket + "/graphs" + newline
    return_str += " - /usr/bin/java -Xmx2048m -Ddir1=$DIR1 -jar /mnt/ebs/otp/lib/graph-builder.jar /mnt/ebs/otp/graph-builder.xml" + newline
    return return_str
    
def writeGraphToS3(bucket) :
    return_str = ""
    return_str += " - /usr/bin/s3put -b " + bucket + " -p /mnt/ebs/otp/" + bucket + "/graphs /mnt/ebs/otp/" + bucket + "/graphs/Graph.obj" + newline
    return return_str

def emailLogAndQuit() :
    return_str = ""
    return_str += " - echo 'run now finished' | /usr/bin/mutt -s 'run_batch complete' -a /var/log/cloud-init.log -- jordan.hare@gmail.com" + newline
    return return_str

def setAwsPerms() :
    accessKey = os.environ.get(access_key_str)
    secretKey = os.environ.get(secret_key_str)
    return_str = ''
    return_str += ' - export ' + access_key_str + "=" + accessKey + newline
    return_str += ' - export ' + secret_key_str + "=" + secretKey + newline
    return return_str

parser = argparse.ArgumentParser(description='specify two directories of GTFS. for each directory, uploaded to S3, create graph.')
parser.add_argument('-dir1', metavar='directory_1', dest='directory_1', help='the first directory to load')
parser.add_argument('-dir2', metavar='directory_2', dest='directory_2', help='the second directory to load')

args = parser.parse_args()

dir1 = trimSlash(args.directory_1)
dir2 = trimSlash(args.directory_2)

dir1_bucket = getBucketName(dir1)
dir1_fileset = getFileSet(dir1)

dir2_bucket = getBucketName(dir2)
dir2_fileset = getFileSet(dir2)

# upload files to S3
#
s3_conn = S3Connection()
uploadToS3(dir1_bucket, dir1_fileset, s3_conn)
#uploadToS3(dir2_bucket, dir2_fileset, s3_conn)

# dynamically construct user data script 
#
user_string = "" 
user_string += base_string 
user_string += setAwsPerms()
user_string += pullFromS3(dir1_bucket, dir1_fileset)
#user_string += pullFromS3(dir2_bucket, dir2_fileset)

user_string += generateGraph(dir1_bucket)
user_string += writeGraphToS3(dir1_bucket)
#user_string += generateGraph(dir2_bucket)
#user_string += writeGraphToS3(dir2_bucket)

user_string += emailLogAndQuit()

print "user data is: " + user_string

#
# start up instance
# pull down S3 data into filesystem
# run graph builder
# post graph object into s3
# shutdown instance
#

ec2_conn = EC2Connection()

ec2_conn.request_spot_instances(price="0.04", 
                                image_id=ami_id, 
                                count=1, 
                                key_name="otp-shadow", 
                                security_groups=["quick-start-1"], 
                                user_data=user_string, 
                                instance_type="m1.large")
