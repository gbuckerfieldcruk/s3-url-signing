# A script to generate a signed URL for an object in S3.
# Designed for backups stored in S3, it'll look for the most recent file in a directory you specify.

import boto3
import argparse
 
parser = argparse.ArgumentParser(description='A script to generate presigned URLs of backup files')
parser.add_argument('-b','--bucket', help='The name of the S3 bucket', required=True)
parser.add_argument('-p','--path', help='The path to look for the backup file', required=True)
parser.add_argument('-P','--profile', help='The AWS credential profile to use', default='default')
parser.add_argument('-t','--timeout', help='The number of seconds until the link expires', type=int, required=True)
 
args = parser.parse_args()
 
session = boto3.Session(profile_name=profile)
 
def get_latest_backupfile(bucket,path):
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket)
    backups = [ ]
    for obj in bucket.objects.filter(Prefix=path):
        backups.append(obj.key)
    latest_file = backups[len(backups)-1]
    return latest_file
 
def generate_url(bucket,key,timeout):
    s3 = session.client('s3')
    url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': bucket,
        'Key': key,
        },
    ExpiresIn=timeout
    )
    return url
 
backupfile = get_latest_backupfile(args.bucket,args.path)
 
backupfile_url = generate_url(args.bucket,backupfile,args.timeout)
 
print backupfile_url
