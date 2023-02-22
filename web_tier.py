"""
    This code uses the Flask framework to create a web server that listens for image files posted to the /image endpoint. 
    When an image file is received, it uploads the file to the input S3 bucket and sends a message to the app tier through SQS. 
    The response to the user is a JSON object containing the SQS message ID.

    We will need to customize this code to match the specifics, such as the names of the S3 buckets and SQS queue, and the endpoint for the app tier.
"""
import boto3
from flask import Flask, request, jsonify
import requests
import json
import os
import pathlib
import yaml

# Create a new Flask app
app = Flask(__name__)

# Set up credentialss
settings_path = pathlib.Path(__file__).parent.parent.parent.absolute() / "settings.yaml"
with open(settings_path, "r") as infile:
        CONFIG = yaml.safe_load(infile)

# put some credentials in the environment
os.environ["AWS_ACCESS_KEY_ID"] = CONFIG["aws_settings"]["AWSAccessKeyID"]
os.environ["AWS_SECRET_ACCESS_KEY"] = CONFIG["aws_settings"]["AWSSecretAccessKey"]
os.environ["AWS_DEFAULT_REGION"] = CONFIG["aws_settings"]["AWSDefaultRegion"]

# Set up the AWS clients
s3 = boto3.client('s3', region_name='us-east-1')
sqs = boto3.resource('sqs', region_name='us-east-1')
queue_name = 'image-recognition-requests'
queue_url = sqs.get_queue_by_name(QueueName=queue_name).url

# Define the endpoint for the app tier
app_tier_endpoint = 'http://app-tier-lb-1234567890.us-east-1.elb.amazonaws.com'

# Define the S3 bucket names for inputs and outputs
input_bucket_name = 'image-recognition-inputs'
output_bucket_name = 'image-recognition-outputs'

# Route for receiving images from users
@app.route('/image', methods=['POST'])
def receive_image():
    # Get the image file from the request
    image_file = request.files['file']

    # Generate a unique filename for the image
    image_filename = str(uuid.uuid4()) + '.jpeg'

    # Upload the image file to the input S3 bucket
    s3.put_object(Bucket=input_bucket_name, Key=image_filename, Body=image_file)

    # Send a message to the app tier to request image recognition
    message = {'image_filename': image_filename}
    sqs_message = sqs.Queue(queue_url).send_message(MessageBody=json.dumps(message))

    # Return the message ID as confirmation
    return jsonify({'message_id': sqs_message.id}), 200

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
