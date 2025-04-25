#!/usr/bin/env python3
import boto3
import requests
import json
import time

BUCKET_NAME = 'menu.tichover.tech' 

def get_s3_policy(client):
    try:
        policy = client.get_bucket_policy(Bucket=BUCKET_NAME)
        policy_json = json.loads(policy['Policy'])
        return policy_json['Statement'][0]['Condition']['IpAddress']['aws:sourceIp']
    except Exception as e:
        print(f"Error fetching the bucket name:\n{e}")
    exit()


def update_s3_policy(client, new_ip):    
    bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
            {
            "Sid": "Restrict-S3-Access-Home-IP",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::menu.tichover.tech/*",
            "Condition": {
                "IpAddress": {
                    "aws:sourceIp": new_ip
                    }
                }
            }
        ]
    }
    policy_json = json.dumps(bucket_policy)

    try:
        client.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=policy_json
        )
        print(f"attempting to update the S3 bucket policy.....")

        for i in range(1,16):
            time.sleep(10)
            if new_ip != get_s3_policy(client):
                print(f"failed to update, attempt {i}/15")
            else:
                print("S3 bucket policy updated successfully!")
                exit()
        print("S3 bucket policy API recieved an update attempt but failed to apply it")

    except Exception as e:
        print(f"Error updating the S3 bucket policy:\n{e}")
