#!/usr/bin/env python3
""" Dynamodb records """
import boto3
import kompass


def handler(event, context):

    # print output
    """ Function get records """
    print('received event:')
    print(context)
    # Variables of this event
    bucket = event['BUCKET']
    local_file_name = event['LOCAL_FILE_NAME']
    s3_file_name = event['S3_FILE_NAME']

    # Scraping Website
    kompass.scraping(local_file_name)

    #Saving in S3
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).upload_file(local_file_name, s3_file_name)
