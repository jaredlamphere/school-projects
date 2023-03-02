import logging
import time
import boto3
from botocore.exceptions import ClientError
# create a DynamoDB client
dynamodb = boto3.client("dynamodb")
TABLE_NAME = 'DogToys'
INDEX_NAME_DT = 'DogToysidIndex'
INDEX_NAME_P = 'PriceIdIndex'

def create_table():

    try:
        db_client = boto3.client('dynamodb')
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

def put_items(table_name, pk,sk,vendor,title,desc,price):
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
          'vendor': {
            'S': vendor,
          },
          'title': {
            'S': title,
          },
          'description': {
            'S': desc,
          },
          'price': {
            'N': str(price), #Note: Even though a number, it is passed as a string
          },
        },
        ReturnConsumedCapacity='TOTAL',
        TableName=TABLE_NAME,
      )        
      return True
    except Exception as e:
        logging.error(e)
        return False
def get_item(table_name, partition_key, sort_key):
    # Get an item from the table
    table = boto3.resource('dynamodb').Table(table_name)
    item = table.get_item(Key={partition_key: partition_key, sort_key: sort_key})
    print(f"Item retrieved: {item.get('Item')}.")

def delete_item(table_name, partition_key, sort_key):
    # Delete an item from the table
    table = boto3.resource('dynamodb').Table(table_name)
    table.delete_item(Key={partition_key: partition_key, sort_key: sort_key})
    print(f"Item with partition key '{partition_key}' and sort key '{sort_key}' deleted.")

dynamodb.delete_table(TableName=TABLE_NAME)
print(f"Table '{TABLE_NAME}' deleted.")

def query_table(table_name, partition_key, sort_key_start, sort_key_end):
    # Query the table for items within a range of the sort key
    table = boto3.resource('dynamodb').Table(table_name)
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key(partition_key).eq(partition_key) & 
                               boto3.dynamodb.conditions.Key(sort_key_start).between(sort_key_start, sort_key_end)
    )
    print(f"Items retrieved: {response['Items']}.")
def delete_table():

    try:
        db_client = boto3.client('dynamodb')
        db_client.delete_table(TableName=TABLE_NAME)
        return True
    except ClientError as e:
        logging.error(e)
        return False

def menu():
    # Main menu for the program
    while True:
        print("\nDynamoDB Menu:")
        print("1. Create Table")
        print("2. Put Items")
        print("3. Get Item")
        print("4. Delete Item")
        print("5. Delete Table")
        print("6. Query Table")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            # Create table
            table_name = input("Enter table name: ")
            partition_key = input("Enter partition key name: ")
            sort_key = input("Enter sort key name: ")
            create_table(table_name, partition_key, sort_key)
        elif choice == "2":
            # Put items
            table_name = input("Enter table name: ")
            items = []
            for i in range(3):
                item = {}
                item[partition_key] = input(f"Enter partition key value for item {i+1}: ")
                item[sort_key] = input(f"Enter sort key value for item {i+1}: ")
                items.append(item)
            put_items(table_name, items)
        elif choice == "3":
            # Get item
            table_name = input("Enter table name: ")
            partition_key = input("Enter partition key value: ")
            sort_key = input("Enter sort key value: ")
            get_item(table_name, partition_key, sort_key)
        elif choice == "4":
            # Delete item
            table_name = input("Enter table name: ")
            partition_key = input("Enter partition key value: ")
            sort_key = input("Enter sort key value: ")
            delete_item(table_name, partition_key, sort_key)
        elif choice == "5":
            # Delete table
            table_name = input("Enter table name: ")
            delete_table(table_name)
        elif choice == "6":
            # Query table
            table_name = input("Enter table name: ")
            partition_key = input("Enter partition key name: ")
            sort_key = input("Enter sort key name: ")
            sort_key_start = input("Enter sort key start value: ")
      

