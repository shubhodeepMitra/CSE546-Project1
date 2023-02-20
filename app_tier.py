"""
    This code should be placed on the EC2 instances running the deep learning model.
    Note: 
        1. Code assumes that the deep learning model script is located at /home/ubuntu/classifier/image_classification.py 
        2. The output file output.txt is generated by that script. 
        3. Modify the paths depending on your setup. 
        4. Also, replace 'your-response-bucket-name' with the name of the S3 bucket where the recognition results will be stored.
"""

import boto3
import subprocess
import os

sqs = boto3.resource('sqs')
request_queue = sqs.get_queue_by_name(QueueName='request_queue')
response_bucket = 'your-response-bucket-name'

while True:
    # Receive messages from the request queue
    messages = request_queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
    if messages:
        # Process each message
        for message in messages:
            image_key = message.body
            image_name = os.path.splitext(os.path.basename(image_key))[0]
            response_key = image_name + '.txt'

            # Run the deep learning model on the image
            subprocess.run(['python3', '/home/ubuntu/classifier/image_classification.py', image_key])

            # Read the result from the output file
            with open('output.txt', 'r') as f:
                result = f.read().strip()

            # Upload the result to S3
            s3 = boto3.resource('s3')
            response_object = s3.Object(response_bucket, response_key)
            response_object.put(Body=result)

            # Delete the message from the queue
            message.delete()
