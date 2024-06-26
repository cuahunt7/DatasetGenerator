import boto3
import os
from dotenv import load_dotenv

def extract_and_upload_metadata(data, algorithm_name, bucket_name, file_path, object_key, target_variable):
    """Extract metadata from the dataset and upload it to DynamoDB."""
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                              region_name=os.getenv('AWS_DEFAULT_REGION'))

    try:
        table = dynamodb.Table('DatasetMetadata')
        dataset_name = input("What is the dataset name? ")
        topic = input("Enter the topic (1 for Health, 2 for Finance, 3 for Entertainment, 4 for Technology, 5 for Education): ")
        topics = {1: "Health", 2: "Finance", 3: "Entertainment", 4: "Technology", 5: "Education"}
        source_link = input("Enter the source link: ")
        size_in_kb = os.path.getsize(file_path) // 1024  # Get file size in kilobytes

        # Now only storing the S3 object key, and not the presigned URL
        response = table.put_item(
            Item={
                'Dataset Name': dataset_name,
                'Machine Learning Task': algorithm_name,
                'Topic': topics[int(topic)],
                'Number of Instances': int(data.shape[0]),
                'Number of Features': int(data.shape[1]),
                'Size in KB': size_in_kb,
                'Source Link': source_link,
                'S3ObjectKey': object_key,  # Storing S3 object key
                'Target Variable': target_variable
            }
        )
        print("Metadata uploaded successfully to DynamoDB.")
    except Exception as e:
        print(f"Failed to upload metadata: {e}")
