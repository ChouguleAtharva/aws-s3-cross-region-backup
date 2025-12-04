import json
import boto3
import logging
from urllib.parse import unquote_plus

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client('s3')

# --- IMPORTANT ---
# Replace this with the actual name of your backup/destination bucket
DESTINATION_BUCKET_NAME = 'my-backup-archive-destination-1234'
# -----------------

def lambda_handler(event, context):
    """
    Handles an S3 event triggered by an object creation (PutObject).
    Copies the newly created object to the destination bucket.
    """
    logger.info("Received event: " + json.dumps(event, indent=2))

    try:
        # Extract bucket and key from the S3 event record
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        # source_key = record['object']['key']
        source_key_encoded = record['object']['key']

        source_key = unquote_plus(source_key_encoded)

        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
        }

        # Copy the object to the destination bucket
        s3_client.copy_object(
            CopySource=copy_source,
            Bucket=DESTINATION_BUCKET_NAME,
            Key=source_key
        )

        logger.info(f"Successfully backed up s3://{source_bucket}/{source_key} to s3://{DESTINATION_BUCKET_NAME}/{source_key}")

        return {
            'statusCode': 200,
            'body': json.dumps('Backup successful!')
        }

    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise e