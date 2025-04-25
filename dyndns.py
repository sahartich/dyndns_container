#!/usr/bin/env python3
import boto3
import requests
import time
from update_s3_policy import update_s3_policy

HOSTED_ZONE_ID = 'Z06121582D2H8GG638YH' 
RECORD_NAME = 'ip.tichover.tech' 
RECORD_TYPE = 'A'

def get_dnsrecord(client):
    try:
        dns_record = client.list_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            StartRecordName=RECORD_NAME,
            StartRecordType=RECORD_TYPE,
            MaxItems='1'
        )
        return dns_record['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
    except Exception as e:
        print(f"Error fetching the DNS record:\n{e}")
    exit()

def update_dns(client, new_ip):
    change_batch = { # json for the record info that will be set
        'Changes': [
            {
                'Action': 'UPSERT',  # updates in place
                'ResourceRecordSet': {
                    'Name': RECORD_NAME,
                    'Type': RECORD_TYPE,
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': new_ip
                        }
                    ]
                }
            }
        ]
    }

    try:
        response = client.change_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            ChangeBatch=change_batch
        )
        print(f"Current IP has changed to {new_ip}, attempting to update the DNS record.....")

        for i in range(1,16):
            time.sleep(10)
            if new_ip != get_dnsrecord(client):
                print(f"failed to update, attempt {i}/15")
            else:
                print("DNS record updated successfully!")
                return True
        print("DNS record API recieved an update attempt but failed to apply it")
        return False

    except Exception as e:
        print(f"Error updating the DNS record:\n{e}")
        return False


def main():
    route53_client = boto3.client('route53')
    s3_client = boto3.client('s3')
    ip_record = get_dnsrecord(route53_client)
    actual_ip = requests.get('https://api.ipify.org').text # fetches via API GET request the public IP

    if ip_record != actual_ip:
        if update_dns(route53_client, actual_ip):
            update_s3_policy(s3_client, actual_ip)
    else:
        print("Nothing to see here")


if  __name__ == '__main__':
    main()
