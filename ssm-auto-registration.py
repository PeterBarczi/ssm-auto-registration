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
            Description = 'MyActivation',
            DefaultInstanceName = 'test',
            IamRole = 'service-role/AmazonEC2RunCommandRoleForManagedInstances',
            RegistrationLimit = 1,
            Tags=[
                {
                    'Key': 'Customer',
                    'Value': 'XYZ'
                },
            ]
        )   
    # I. Stores Output into file
    #with open('/tmp/reg-creds', 'w') as f:
    #    print(resp, file=f)
    #
    # II. Print Output
    #print(resp)
    #
    # III. Upload output file to S3
    #s3 = boto3.resource(service_name = 's3')
    #s3.meta.client.upload_file(Filename = '/tmp/reg-creds', Bucket = 'tsy-vmc-dev-s3-euc1-test', Key = 'reg-creds')
    #
    # IV. Parse Output directly
    id = resp.get("ActivationId")
    code = resp.get("ActivationCode")
    print(id)
    print(code)
    
    # Part II
    client = boto3.client('route53')
    
    response = client.change_resource_record_sets(
    HostedZoneId='Z0797032DCH5FW0MZB7P',
    ChangeBatch={
        'Comment': 'Add entries',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'code.big-data.sk.',
                    'ResourceRecords': [
                        {
                            'Value': "\"5Pib5OW9nBFs57ddVqvLkzx\"",
                        },
                    ],
                    'TTL': 60,
                    'Type': 'TXT',
                },
            },
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'id.big-data.sk.',
                    'ResourceRecords': [
                        {
                            'Value': "\"new\"",
                        },
                    ],
                    'TTL': 60,
                    'Type': 'TXT',
                },
            },
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'region.big-data.sk.',
                    'ResourceRecords': [
                        {
                            'Value': "\"myregion\"",
                        },
                    ],
                    'TTL': 60,
                    'Type': 'TXT',
                },
            },
        ],
    },
    )
