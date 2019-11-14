import json
import googlemaps
from datetime import datetime
import os
import boto3

env = os.environ

def lambda_handler(event, context):
    gmaps = googlemaps.Client(key=env['google_key'])

    now = datetime.now()
    directions_result_home = gmaps.distance_matrix(env['start_1'],
                                     env['end_1'],
                                     mode="driving",
                                     avoid="tolls",
                                     departure_time=now)

    directions_result_school = gmaps.distance_matrix(env['start_2'],
                                     env['end_2'],
                                     mode="driving",
                                     avoid="tolls",
                                     departure_time=now)

    return_body = {
        "journey": env["journey_type"],
        "route1": {
            "full_result": directions_result_home,
            "duration": directions_result_home['rows'][0]["elements"][0]["duration"]["value"],
            "duration_in_traffic": directions_result_home['rows'][0]["elements"][0]["duration_in_traffic"]["value"]
        },
        "route2": {
            "full_result": directions_result_school,
            "duration": directions_result_school['rows'][0]["elements"][0]["duration"]["value"],
            "duration_in_traffic": directions_result_school['rows'][0]["elements"][0]["duration_in_traffic"]["value"]
        }
    }

    print(return_body)

    s3 = boto3.client('s3')

    response = s3.put_object(
        Bucket="travel-time-data",
        Key="data/{}/{}/{}/{}.json".format(now.year, now.month, now.day, "{}{}{}".format(now.hour, now.minute, now.second)),
        Body=json.dumps(return_body),
        ACL='bucket-owner-full-control'
    )
    return response
