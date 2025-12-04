import json
import boto3
import logging
# Import the URL parsing library (The fix!)
from urllib.parse import unquote_plus 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- IMPORTANT: Ensure this is your Destination Bucket Name ---
DESTINATION_BUCKET_NAME = 'my-backup-archive-destination-1234'
# -----------------------------------------------------------

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Handles an S3 event triggered by an object deletion.
    Decodes the key and deletes the corresponding object in the destination bucket.
    """
    try:
        # 1. Extract the key (which S3 sends as URL-encoded)
        record = event['Records'][0]['s3']
        source_key_encoded = record['object']['key']
        
        # 2. URL DECODE THE KEY so it matches the object name in the destination
        source_key = unquote_plus(source_key_encoded)
        
        # 3. Delete the object from the destination bucket
        s3_client.delete_object(
            Bucket=DESTINATION_BUCKET_NAME,
            Key=source_key # Use the DECODED key for deletion
        )
        
        logger.info(f"Successfully deleted {source_key} from s3://{DESTINATION_BUCKET_NAME}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Deletion successful!')
        }

    except Exception as e:
        logger.error(f"Error processing deletion event: {e}")
        # Note: In a production system, you might not raise an exception 
        # on delete if the file is already gone, but we raise it here for debugging.
        raise e