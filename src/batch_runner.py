'''
Created on Nov 27, 2012

@author: hare
'''



'''
read "base" files out of filesystem and store in S3 under base-key
read "modified" files out of the filesystem and store in S3 under modify-ke

spawn on-demand AWS instances
read "base", "modified"  from S3 and generate base-graph and modify-graph, storing in S3
spawn on-demand AWS instances
run OTP Analyst Batch on base-graph and generate base-tiff, storing in S3
run OTP Analyst Batch on modify-graph and generate modify-tiff, storing in S3
'''



from boto.s3.connection import S3Connection
from boto.s3.key import Key

_AWS_ACCESS_KEY = "AKIAJ4YM7LJUTBFMED6A"
_AWS_SECRET_KEY = "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"

base_path = "/otp/cache/nyc-hacked/"
modify_path = "/otp/cache/nyc-hacked/"

conn = S3Connection(_AWS_ACCESS_KEY, _AWS_SECRET_KEY)
bucket = conn.create_bucket("test_bucket_otp_analyst")  

bronx = Key(bucket)
brooklyn = Key(bucket)
manhattan = Key(bucket)
queens = Key(bucket)
staten = Key(bucket)
busco = Key(bucket)
lirr = Key(bucket)
mnrr = Key(bucket)
subway = Key(bucket)


'''
dispatch unchanged GTFS files to S3
'''

bronx.key = "bronx_base"
bronx.set_contents_from_filename(base_path + "bronx.zip")

brooklyn.key = "brooklyn_base"
brooklyn.set_contents_from_filename(base_path + "brooklyn.zip")

manhattan.key = "manhattan_base"
manhattan.set_contents_from_filename(base_path + "manhattan.zip")

queens.key = "queens_base"
queens.set_contents_from_filename(base_path + "queens.zip")

staten.key = "staten_base"
staten.set_contents_from_filename(base_path + "staten.zip")

busco.key = "busco_base"
busco.set_contents_from_filename(base_path + "busco.zip")

lirr.key = "lirr_base"
lirr.set_contents_from_filename(base_path + "lirr.zip")

mnrr.key = "mnrr_base"
mnrr.set_contents_from_filename(base_path + "mnrr.zip")

subway.key = "subway_base"
subway.set_contents_from_filename(base_path + "subway.zip")



