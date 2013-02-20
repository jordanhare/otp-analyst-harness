'''
Created on Dec 5, 2012

@author: hare

NOTE: not executable
'''

from boto.s3.key import Key
import os

access_key_str = "AWS_ACCESS_KEY_ID"
secret_key_str = "AWS_SECRET_ACCESS_KEY"

s3copy_string = " - /usr/bin/java -jar /home/ec2-user/s3cp/s3cp-cmdline-0.1.11.jar "
homedir = "/home/ec2-user/"

zip_pattern = "/*.zip"
all_pattern = "/*.*"

newline = "\n"

base_string = """#cloud-config
 
runcmd:
 - set -x
 - mount /dev/sdf1 /mnt/ebs 
 - export HOME=/home/ec2-user
"""

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

def getBucketName(dirname) :
    return dirname.split("/")[-1]

def generateGraph(bucket) :
    return_str = ""
    return_str += " - export DIR1=" + bucket + newline
    return_str += " - /usr/bin/java -Xmx4096m -Ddir1=$DIR1 -jar " + \
        "/mnt/ebs/OpenTripPlanner/opentripplanner-graph-builder/target/graph-builder.jar " + \
        "/mnt/ebs/config/graph-generator.xml" + newline
    return return_str

def generateAnalystImage(bucket, date, time, searchCutOff, thresholdAccum, thresholdAgg, maxWalkDist, origin, tiffname) :
    return_str = ""
    return_str += " - export DIR1=" + bucket + newline
    return_str += " - export DATE=" + date + newline
    return_str += " - export TIME='" + time + "'" + newline
    return_str += " - export SEARCHCUTOFF=" + searchCutOff + newline
    return_str += " - export THRESHOLDACCUM=" + thresholdAccum + newline
    return_str += " - export THRESHOLDAGG=" + thresholdAgg + newline
    return_str += " - export MAXWALKDIST=" + maxWalkDist + newline
    return_str += " - export ORIGIN=" + origin + newline
    return_str += " - export TIFFNAME=" + tiffname + newline
    return_str += " - mkdir /home/ec2-user/" + bucket + "/nyc" + newline
    return_str += " - mv /home/ec2-user/" + bucket + "/Graph.obj /home/ec2-user/" + bucket + "/nyc/Graph.obj" + newline
    return_str += " - /usr/bin/java -Xmx4096m " + \
        "-Ddir1=$DIR1 -Ddate=$DATE -Dtime=$TIME -DsearchCutOff=$SEARCHCUTOFF " + \
        "-DthresholdAccum=$THRESHOLDACCUM -DthresholdAgg=$THRESHOLDAGG " + \
        "-DmaxWalkDist=$MAXWALKDIST -Dorigin=$ORIGIN -Dtiffname=$TIFFNAME " + \
        "-jar /mnt/ebs/OpenTripPlanner/opentripplanner-analyst/target/otp-analyst.jar /mnt/ebs/config/batchAnalystConfig.xml" + newline
    return return_str

def pullFromS3(bucket, file_set, useOriginalFiles=False) :
    return_str = ""
    return_str += " - mkdir /home/ec2-user/" + bucket + newline
    for f in file_set :
        if useOriginalFiles == True :
            return_str += s3copy_string + "s3://" + bucket + "/" + f + " " + homedir + bucket + "/" + f + newline
        else :
            f_short = getFileName(f)        
            return_str += s3copy_string + "s3://" + bucket + "/" + f_short + " " + homedir + bucket + "/" + f_short + ".zip" + newline
    return return_str

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

def writeGraphToS3(bucket) :
    return_str = ""
    return_str += " - /usr/bin/s3put -b " + bucket + " -p /home/ec2-user/" + bucket + " /home/ec2-user/" + bucket + "/Graph.obj" + newline
    return return_str

def writeAnalystImageToS3(bucket, tiffname) :
    return_str = ""
    return_str += " - /usr/bin/s3put -b output_images -p /home/ec2-user/" + bucket + \
        " /home/ec2-user/" + bucket + "/" + tiffname + ".tiff" + newline
    return return_str

def getFileName (longFileName) :
    return longFileName.split("/")[-1].split(".")[0]

def trimSlash(dirname) :
    if (dirname[-1:] == "/") :
        return dirname.rstrip("/")
    else :
        return dirname

def spawnAwsInstance (ec2_conn, ami_id, user_string) :
    print "user data is: " + user_string
    ec2_conn.request_spot_instances(price="0.10", 
                                    image_id=ami_id, 
                                    count=1, 
                                    key_name="otp-shadow", 
                                    security_groups=["quick-start-1"], 
                                    user_data=user_string, 
                                    instance_type="m1.xlarge")
