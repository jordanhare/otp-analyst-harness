'''
Created on Nov 20, 2012

@author: hare
'''

from boto.s3.connection import S3Connection
from boto.s3.key import Key



_AWS_ACCESS_KEY = "AKIAJ4YM7LJUTBFMED6A"
_AWS_SECRET_KEY = "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"

conn = S3Connection(_AWS_ACCESS_KEY, _AWS_SECRET_KEY)
bucket = conn.create_bucket("test_bucket_otp_analyst")

#k = Key(bucket)

bronx = Key(bucket)
brooklyn = Key(bucket)
manhattan = Key(bucket)
queens = Key(bucket)
staten = Key(bucket)

busco = Key(bucket)
lirr = Key(bucket)
mnrr = Key(bucket)
subway = Key(bucket)


bronx.key = "bronx"

bronx.set_contents_from_filename("/otp/cache/nyc-hacked/bronx.zip")



#k.key = "foobar"
#k.set_contents_from_string("isn't s3 great")





# print "results are: " + k.get_contents_as_string()