"""
S3 File Sorter Lambda Function

This Lambda function automatically sorts files uploaded to an S3 bucket:
- Numeric filenames (e.g., 123.txt) → Destination2
- Non-numeric filenames (e.g., report.doc, 1aws.txt) → Destination1

Author: Umama Aemun
Date: 2025-09-29
"""

import boto3
import json
import urllib.parse
import os
import re
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')


def lambda_handler(event, context):
    """
    Main Lambda handler function triggered by S3 events
    
    Args:
        event: S3 event containing bucket and object information
        context: Lambda context object
        
    Returns:
        dict: Response with status code and message
    """
    try:
        # Get destination buckets from environment variables
        destination1_bucket = os.environ['DESTINATION1_BUCKET']
        destination2_bucket = os.environ['DESTINATION2_BUCKET']
        
        logger.info(f"Destination1: {destination1_bucket}")
        logger.info(f"Destination2: {destination2_bucket}")
        
        # Process each record in the event
        for record in event['Records']:
            # Extract bucket and object information
            source_bucket = record['s3']['bucket']['name']
            object_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
            
            logger.info(f"Processing file: {object_key} from bucket: {source_bucket}")
            
            # Extract filename from the full path
            filename = object_key.split('/')[-1]
            logger.info(f"Filename: {filename}")
            
            # Get filename without extension for pattern matching
            filename_without_ext = os.path.splitext(filename)[0]
            logger.info(f"Filename without extension: {filename_without_ext}")
            
            # Determine destination based on filename pattern
            # Pattern ^[0-9]+$ matches ONLY numeric characters
            if re.match(r'^[0-9]+$', filename_without_ext):
                destination_bucket = destination2_bucket
                logger.info(f"✅ File '{filename}' has NUMERIC name → Moving to DESTINATION2")
            else:
                destination_bucket = destination1_bucket
                logger.info(f"✅ File '{filename}' has NON-NUMERIC name → Moving to DESTINATION1")
            
            # Copy object to destination bucket
            copy_source = {
                'Bucket': source_bucket,
                'Key': object_key
            }
            
            logger.info(f"Copying from s3://{source_bucket}/{object_key} to s3://{destination_bucket}/{object_key}")
            
            s3.copy_object(
                CopySource=copy_source,
                Bucket=destination_bucket,
                Key=object_key
            )
            
            logger.info(f"✅ Successfully copied {object_key} to {destination_bucket}")
            
            # Delete the original file from source bucket
            logger.info(f"Deleting original file from source bucket")
            
            s3.delete_object(
                Bucket=source_bucket,
                Key=object_key
            )
            
            logger.info(f"✅ Successfully deleted {object_key} from {source_bucket}")
            logger.info(f"--- File processing completed for {filename} ---")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Files processed successfully')
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing files: {str(e)}")
        logger.error(f"Event: {json.dumps(event)}")
        raise e


def is_numeric_filename(filename):
    """
    Helper function to check if filename is purely numeric
    
    Args:
        filename (str): Filename without extension
        
    Returns:
        bool: True if filename contains only digits, False otherwise
        
    Examples:
        >>> is_numeric_filename("123")
        True
        >>> is_numeric_filename("1aws")
        False
        >>> is_numeric_filename("report")
        False
    """
    return bool(re.match(r'^[0-9]+$', filename))
