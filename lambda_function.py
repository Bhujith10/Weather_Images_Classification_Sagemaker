import json
import boto3
import base64
import os

s3=boto3.client('s3')

ENDPOINT = 'image-classification-2023-03-14-17-44-15-030'

runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    
    file_path = os.path.join('/tmp', 'image.png')
    with open(file_path, 'wb') as f:
        s3.download_fileobj(bucket, key, f)
    
    with open("/tmp/image.png", "rb") as f:
        image_data = f.read()
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,
                                       ContentType='image/png',
                                       Body=image_data)

    
    result = json.loads(response['Body'].read().decode())
    
    classes = ["cloudy", "rain", "shine", "sunrise"]
    
    prediction = classes[result.index(max(result))]
    
    # We return the data back to the Step Function    
    event["prediction_probabilites"] = result
    event["prediction"] = prediction
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
    
