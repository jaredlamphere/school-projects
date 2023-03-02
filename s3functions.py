import logging
import requests
import io
import boto3
from botocore.exceptions import ClientError
###############################################################################
# Create an S3 bucket in a specified region.
###############################################################################
def create_bucket(bucket_name, region):
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
    except ClientError as e:
        logging.error(e)
        return False
    
    return True
###############################################################################
# Retrieve the list of existing buckets
###############################################################################
def list_all_buckets():
    
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
    except ClientError as e:
        logging.error(e)
        return False
    # Output the bucket names
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    
    return True
###############################################################################
# Upload a file to a bucket
###############################################################################
def upload_file(bucket_name, file_name, object_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
###############################################################################
# Upload binary data to a bucket
# Will automatically handle multipart uploads behind the scenes if necessary.
###############################################################################
def upload_file_obj(bucket_name, file_name, binary_data):
    
    try:
        s3_client = boto3.client('s3')
        fo = io.BytesIO(binary_data)
        s3_client.upload_fileobj(fo, bucket_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
###############################################################################
# Put an object - lower level API call
# Does not do multi-part uploads
###############################################################################
def put_object(bucket_name, object_name, file_name):
    try:
        s3_client = boto3.client('s3')
        with open(file_name, 'rb') as f:
            content = f.read()
        # Send the to the bucket
        s3_client.put_object(Body=content, Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Download a file to the loacal hard drive - upper level API call 
# Will automatically handle multipart downloads behind the scenes if necessary.
###############################################################################
def download_file(bucket_name, object_name, file_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket_name, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Download a file and save to a file-like object
# Will automatically handle multipart downloads behind the scenes if necessary.
###############################################################################
def download_file_object(bucket_name, object_name, fob):
    try:
        s3_client = boto3.client('s3')
        s3_client.download_fileobj(bucket_name, object_name, fob)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Get an object - lower level API call.
# Does not do multi-part downloads
###############################################################################
def get_object(bucket_name, object_name, file_name):
    try:
        s3_client = boto3.client('s3')
        s3_response_object = s3_client.get_object(Bucket=bucket_name, 
Key=object_name)
        # Get the "StreamingBody"...
        object_content = s3_response_object['Body'].read()
        
        #Push the "StreamingBody" stream to a file.
        with open(file_name, 'wb') as f:
            f.write(object_content)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# List all objects in a bucket.
# Uses paginators. 
#See:https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
###############################################################################
def list_all_objects(bucket_name):
    try:
        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket_name):
            for content in page["Contents"]:
                key = content['Key']    
                print(key)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Delete an object in a bucket.
###############################################################################
def delete_object(bucket_name, object_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Delete all objects in a bucket.
# Uses paginators. 
#See:https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
###############################################################################
def delete_all_objects(bucket_name):
    try:
        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket_name):
            for content in page["Contents"]:
                key = content['Key']    
                s3_client.delete_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Delete a bucket.
###############################################################################
def delete_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True        
###############################################################################
# Generate a presigned URL to share an S3 object
###############################################################################    
def create_presigned_url(bucket_name, object_name, expiration=3600):
    
    try:
        s3_client = boto3.client('s3')
        Params={'Bucket': bucket_name,'Key': object_name}
        url = s3_client.generate_presigned_url('get_object', Params, 
ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None, None
    # Optional - Get the file via the presigned URL.
    if url is not None:
      return url, requests.get(url).content
    return None, None
###############################################################################
## Query the internals of an S3 object.
###############################################################################
def s3_select(bucket_name, file_name, expression):
    try:
        s3_client = boto3.client("s3")
        bucket = bucket_name
        key = file_name
        expression_type = "SQL"
        expression = expression
        input_serialization = {"CSV": {"FileHeaderInfo": "USE"}}
        output_serialization = {"JSON": {}}
        response = s3_client.select_object_content(
            Bucket=bucket,
            Key=key,
            ExpressionType=expression_type,
            Expression=expression,
            InputSerialization=input_serialization,
            OutputSerialization=output_serialization
        )
    except ClientError as e:
        logging.error(e)
        return False
    for event in response["Payload"]:
        print(event)
    
    return True
###############################################################################
# Exercise the S3 functions.
###############################################################################
def main():
    region ='us-east-1'
    bucket_name = input("Please enter bucket name: ")
    upload_file_name_csv = 'deniro.csv'
    upload_file_name_name_txt = 'some_data.txt'
    download_file_name_txt = 'some_data2.txt'
    # sql_espression = """SELECT * FROM S3Object"""
    sql_espression = """SELECT s.Title FROM S3Object s"""
    
    ####
    list_all_buckets()
    
    create_bucket(bucket_name,region)
    list_all_buckets()
    
    upload_file(bucket_name, upload_file_name_csv, upload_file_name_csv)
    
    list_all_objects(bucket_name)
    delete_object(bucket_name, upload_file_name_csv)
    
    upload_file_obj(bucket_name, upload_file_name_name_txt, b'This is some data')
    
    delete_object(bucket_name, upload_file_name_name_txt)
    put_object(bucket_name,upload_file_name_csv,upload_file_name_csv)
    download_file(bucket_name, upload_file_name_csv, download_file_name_txt)
    
    with open(download_file_name_txt, 'wb') as f:
        download_file_object(bucket_name, upload_file_name_csv, f)
    
    get_object(bucket_name, upload_file_name_csv, download_file_name_txt)
    
    url, data = create_presigned_url(bucket_name, upload_file_name_csv)
    s3_select(bucket_name,upload_file_name_csv,sql_espression)
    
    delete_all_objects(bucket_name)
    
    delete_bucket(bucket_name)
###############################################################################
# Exercise the S3 functions.
###############################################################################
main()