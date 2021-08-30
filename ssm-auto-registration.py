import json
import boto3
import socket
import sys

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('ssm')
    # Get hostname
    hostname = socket.getfqdn()
    # Activation
    resp = client.create_activation(
           #Description = socket.getfqdn(),
            Description = 'TestingActivation',
            DefaultInstanceName = 'test',
            IamRole = 'service-role/AmazonEC2RunCommandRoleForManagedInstances',
            RegistrationLimit = 100,
            Tags=[
                {
                    'Key': 'Customer',
                    'Value': 'X'
                },
            ]
        )   
    # Stores Output into file
    with open('/tmp/reg-creds', 'w') as f:
        print(resp, file=f)
    #
    # Print Output
    print(resp)
    #
    # Upload output file to S3
    s3 = boto3.resource(service_name = 's3')
    s3.meta.client.upload_file(Filename = '/tmp/reg-creds', Bucket = 'tsy-vmc-dev-s3-euc1-test', Key = 'reg-creds')
