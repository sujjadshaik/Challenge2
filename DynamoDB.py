import boto3
from pprint import pprint

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name='eu-west-1')

    table = dynamodb.create_table(
        TableName='Employee',
        KeySchema=[
            {
                'AttributeName': 'emp_image_name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'emp_id',
                'KeyType': 'RANGE'  # Sort key
            }

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'emp_image_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'emp_id',
                'AttributeType': 'S'
            },


        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

def delete_emp_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name='eu-west-1')

    table = dynamodb.Table('Employee')
    table.delete()


def insert_emp_details(emp_id,emp_name,emp_phone,emp_email,emp_address,emp_image_name,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name='eu-west-1')

    table = dynamodb.Table('Employee')
    response = table.put_item(
        Item={
            'emp_id' : emp_id,
            'emp_name' : emp_name,
            'emp_phone' : emp_phone,
            'emp_email' : emp_email,
            'emp_address' : emp_address,
            'emp_image_name' : emp_image_name
            }
    )
    return response


def read(face_name):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",region_name='us-west-2')
    table = dynamodb.Table('Employee')
    response = table.query(
        KeyConditionExpression=Key('emp_image_name').eq(face_name)
    )
    return response['Items']

def tabel_data():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",region_name='us-west-2')
    table = dynamodb.Table("Employee")
    items = table.scan()['Items']
    for item in items:
        print (item)
