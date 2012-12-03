#!/usr/bin/python

'''
Created on Nov 27, 2012

@author: hare
'''

from boto.s3.connection import S3Connection
from boto.ec2.connection import EC2Connection

from boto.s3.key import Key
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType

import argparse
import glob
import sys

def trimSlash(dirname) :
    if (dirname[-1:] == "/") :
        return dirname.rstrip("/")
    else :
        return dirname

def uploadToS3(dirname, sql_conn) :
    file_set = glob.glob(dirname + match_pattern)
    bucket_name = dirname.split("/")[-1]
    bucket = sql_conn.create_bucket(bucket_name)
    bucket.set_acl('public-read')
    print "dirname " + dirname + " stored into bucket " + bucket_name 
    for file_entry in file_set :
        file_short = file_entry.split("/")[-1].split(".")[0]
        key = Key(bucket)
        key.key = file_short
        print "storing as key: " + file_short
        key.set_contents_from_filename(file_entry)        
        key.set_acl('public-read')

match_pattern = "/*.zip"
ami_id = "ami-8d75f5e4"

graph_gen_script = open("/Users/hare/eclipse_workspace/batch-analyst-runner/src/cloud-init/base_proof2.sh")

parser = argparse.ArgumentParser(description='specify two directories of GTFS. for each directory, uploaded to S3, create graph.')
parser.add_argument('-dir1', metavar='directory_1', dest='directory_1', help='the first directory to load')
parser.add_argument('-dir2', metavar='directory_2', dest='directory_2', help='the second directory to load')

args = parser.parse_args()

dir1 = trimSlash(args.directory_1)
dir2 = trimSlash(args.directory_2)

#
# establish connection to S3
#
sql_conn = S3Connection()


#
# upload files to S3
#
uploadToS3(dir1, sql_conn)
uploadToS3(dir2, sql_conn)

#sys.exit()

# kick off graph-builder instances
ec2_conn = EC2Connection()

#instance_list = ["i-63a4a31c"]
#
#reservation_list = ec2_conn.get_all_instances(instance_list)
#
#reserve = reservation_list[0]
#
#instances = reserve.instances
#
#instance = instances[0]
#
#instance.start()

#print "class is:" + str(reservation_list[0].__class__)
#print "class is:" + str(instances[0].__class__)
#sys.exit()

shared_drive = BlockDeviceType(connection=ec2_conn, volume_id="vol-fad4dd86")

block_device_mapping = BlockDeviceMapping()
block_device_mapping["/dev/sdf"] = shared_drive

#block_device_mapping = {  : "vol-fad4dd86"}


#ec2_conn.run_instances(image_id=ami_id, 
#                       instance_type="t1.micro", 
#                       security_groups=["full-access"], 
#                       key_name="otp-shadow", 
#                       placement="us-east-1d"
#                       block_device_map=block_device_mapping 
#                       user_data=graph_gen_script.read()
#                       )


ec2_conn.request_spot_instances(price="0.04", 
                                image_id=ami_id, 
                                count=1, 
                                key_name="otp-shadow", 
                                security_groups=["quick-start-1"], 
                                user_data=graph_gen_script.read(), 
                                instance_type="m1.large")

## unused
#type, valid_from, 
#valid_until, launch_group, 
#availability_zone_group,  addressing_type, 
#placement, kernel_id, 
#ramdisk_id, monitoring_enabled, 
#subnet_id, placement_group, 
#block_device_map, instance_profile_arn, 
#instance_profile_name, security_group_ids, ebs_optimized 


