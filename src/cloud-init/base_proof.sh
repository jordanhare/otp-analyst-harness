#!/bin/sh

echo "Hello World.  The time is now $(date -R)!" | tee /root/output.txt
mount /dev/sdf1 /mnt/ebs

wget -O /home/ec2-user/s3cp.zip http://beaconhill.com/downloader/get.htm?key=s3cp.zip
/usr/bin/unzip /home/ec2-user/s3cp.zip

