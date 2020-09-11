import json
from datetime import datetime, timedelta
import os
import boto3
import pytz
import csv


env = os.environ

def lambda_handler(event, context):
    now = datetime.now() - timedelta(1)
    s3 = boto3.resource('s3')
    temp_csv_file = ""

    bucket = s3.Bucket('travel-time-data')
    prefix_objs = bucket.objects.filter(Prefix="data/{}/{}/{}".format(now.year, now.month, now.day))
    for obj in prefix_objs:
        data = json.loads(obj.get()['Body'].read())
        temp_csv_file+="{},{},{}\n".format(
            convert_time_to_EST(obj.last_modified).strftime('%H:%M:%S'),
            data["route1"]["duration_in_traffic"],
            data["route2"]["duration_in_traffic"]
        )

    client = boto3.client('s3')
    response = client.put_object(
        Bucket="travel-time-data",
        Key="merged_data/{}.csv".format("{}{}{}".format(now.year, now.month, now.day)),
        Body=temp_csv_file,
        ACL='bucket-owner-full-control'
    )

    return response

def convert_time_to_EST(time):
    eastern = pytz.timezone('US/Eastern')
    return time.astimezone(eastern)
