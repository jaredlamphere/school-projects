import logging
import time
import boto3
from botocore.exceptions import ClientError
ENDPOINT = 'http://localhost:8000'


TABLE_NAME = 'Guitar'
INDEX_NAME_DT = 'GuitarBrandidIndex'
INDEX_NAME_P = 'PriceIdIndex'


# Create a DynamoDb Table.
###############################################################################
def create_table():

    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        db_client.create_table(
          AttributeDefinitions=[
             {
                  'AttributeName': 'pk',
                  'AttributeType': 'S',
              },
              {
                  'AttributeName': 'sk',
                  'AttributeType': 'S',
              },
              {
                  'AttributeName': 'price',
                  'AttributeType': 'N',
              }
          ],
          KeySchema=[
              {
                  'AttributeName': 'pk',
                  'KeyType': 'HASH',
              },
              {
                  'AttributeName': 'sk',
                  'KeyType': 'RANGE',
              }
          ],
          ProvisionedThroughput={
              'ReadCapacityUnits': 2,
              'WriteCapacityUnits': 2,
          },
          GlobalSecondaryIndexes=[
          {
                'IndexName': INDEX_NAME_DT,
                'KeySchema': [
                    {
                        'AttributeName': 'sk',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'pk',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': INDEX_NAME_P,
                'KeySchema': [
                    {
                      'AttributeName': 'sk',
                      'KeyType': 'HASH'
                    },
                    {
                      'AttributeName': 'price',
                      'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
          ],
          TableName=TABLE_NAME,
        )
        return True
    except ClientError as e:
        logging.error(e)
        return False
###############################################################################
# Describe a DynamoDb Table.
###############################################################################
def describe_table():

    try:
        db_client = boto3.client('dynamodb')
        response = db_client.describe_table(TableName=TABLE_NAME)
        return response['Table']['TableStatus']
    except ClientError as e:
        logging.error(e)
        return None
###############################################################################
# Delete a DynamoDb Table.
###############################################################################
def delete_table():

    try:
        db_client = boto3.client('dynamodb')
        db_client.delete_table(TableName=TABLE_NAME)
        return True
    except ClientError as e:
        logging.error(e)
        return False
###############################################################################
# Put a DynamoDb Item.
###############################################################################
def put_item(pk,sk,brand,model,desc,price):

    try:
      db_client = boto3.client('dynamodb')
      db_client.put_item(
        Item={
          'pk': {
            'S': pk,
          },
          'sk': {
            'S': sk,
          },
          'brand': {
            'S': brand,
          },
          'model': {
            'S': model,
          },
          'description': {
            'S': desc,
          },
          'price': {
            'N': str(price), 
          },
        },
        ReturnConsumedCapacity='TOTAL',
        TableName=TABLE_NAME,
      )        
      return True
    except Exception as e:
        logging.error(e)
        return False
###############################################################################
# Get a DynamoDb Item.
###############################################################################
def get_item(pk,sk):

    try:
      db_client = boto3.client('dynamodb')
      response = db_client.get_item(
        Key={
          'pk': {
            'S': pk,
          },
          'sk': {
              'S': sk,
          },      
        },
        TableName=TABLE_NAME,
      )
      return response["Item"]
    except ClientError as e:
        logging.error(e)
        return None
###############################################################################
# Query a DynamoDb table.
# https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html#DDB-Query-request-KeyConditionExpression
###############################################################################
def query():

    try:
      db_client = boto3.client('dynamodb')
      response = db_client.query(
          ExpressionAttributeValues={
              ':v1': {
                  'S': 'guitar',
              },
              ':v2': {
                  'N': '1',
              },
              ':v3': {
                  'N': '2',
              }
          },
          #KeyConditionExpression='sk = :v2 AND pk = :v1',
          KeyConditionExpression='sk = :v1 AND price BETWEEN :v2 AND :v3',
          #KeyConditionExpression='sk = :v2 AND begins_with(pk,:v1)',
          ProjectionExpression='title, vendor, price',
          TableName = TABLE_NAME,
          IndexName = INDEX_NAME_P
      )
      return response["Items"]
    except Exception as e:
        logging.error(e)
        return None  
###############################################################################
# Query a DynamoDb table.
# https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html#DDB-Query-request-KeyConditionExpression
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html
###############################################################################
def scan():

    try:
      db_client = boto3.client('dynamodb')
      response = db_client.scan(
          ExpressionAttributeNames={
              '#p': 'price',
              '#b': 'brand',
              '#m': 'model'
          },
          ExpressionAttributeValues={
              ':v1': {
                  'S': 'dt',
              },
              # ':v2': {
              #     'N': '1',
              # },
              # ':v3': {
              #     'N': '10',
              # }
          },
          #FilterExpression='pk = :v1',
          FilterExpression='begins_with(pk,:v1)',
          #FilterExpression='#p BETWEEN :v2 AND :v3',
          ProjectionExpression='#p, #v, #t',
          TableName=TABLE_NAME,
      )
      return response['Items']
    except ClientError as e:
        logging.error(e)
        return None   
###############################################################################
# Exercise the DynamoDb functions.
###############################################################################
def main():

  create_table()

  while True:
    results = describe_table()
    if results == 'ACTIVE':
      break
    time.sleep(10)

  #Add 3 items...
  put_item('dt1',"DogTreat","Chewy Treats Inc.","Super Chewy - Plain","A super yummy, plain flavored treat!",9.99)
  put_item('dt2',"DogTreat","Chewy Treats Inc.","Super Chewy - Mint","A super yummy, mint flavored treat!",1.59)
  put_item('dt3',"DogTreat","Chewy Treats Inc.","Super Chewy - Juicy Fruit","A super yummy, juicy fruit flavored treat!",2.19)

  # Fix mistake on first item (overwrite the price)...
  put_item('dt1',"DogTreat","Chewy Treats Inc.","Super Chewy - Plain","A super yummy, plain flavored treat!",.99)
  item = get_item('dt1',"DogTreat") 
  print('Item:', item)
  print(item['vendor']['S'])

  # Add 3 more items...
  put_item('toy1',"small","DogToys R Us Inc.","Rubber Ball","A small rubber ball!",4.99)
  put_item('toy2',"medium","DogToys R Us Inc.","Rubber Ball","A medium rubber ball!",10.99)
  put_item('toy3',"large","DogToys R Us Inc.","Rubber Ball","A large rubber ball!",16.99)

  items = query()
  for item in items:
    print(item)

  delete_table()
###############################################################################
# Exercise the DynamoDb functions.
###############################################################################
main()

