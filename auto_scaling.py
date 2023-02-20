"""
    Design to CloudWatch to scale EC2 instances based on the size of an SQS queue:
    1. Create an Amazon CloudWatch alarm for the SQS queue. This alarm should be based on the "ApproximateNumberOfMessagesVisible" metric,
        which gives the number of messages that are currently visible in the queue.
        Set the threshold for the alarm based on the desired scaling behavior. For example, you might set the alarm threshold to 100 messages,
        so that the alarm is triggered whenever the queue size exceeds this number.
    2. Create a new Amazon EC2 Auto Scaling group for your application instances. This group should have a launch configuration that specifies the AMI and
        instance type that you want to use for your instances.
        You can also specify any other configuration details that you need for your instances, such as security groups or IAM roles.
    3. Configure the Auto Scaling group to use the CloudWatch alarm that you created in step 1. 
        You can do this by adding the alarm as a scaling policy for the group. When the alarm is triggered, the scaling policy will be activated,
        and the Auto Scaling group will launch new instances to handle the increased load.
    4. Set the desired capacity for the Auto Scaling group. This is the number of instances that you want to have running at any given time.
        You can set this value based on the expected demand for your application, or you can use other factors to determine the appropriate capacity level.
    5. Monitor the SQS queue and adjust the desired capacity of the Auto Scaling group as needed. 
        You can do this manually, or you can use automation tools such as AWS Lambda functions to adjust the capacity automatically based on the queue size.
"""

import boto3

# create a new CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# create an alarm for the SQS queue
response = cloudwatch.put_metric_alarm(
    AlarmName='queue-size-alarm',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='ApproximateNumberOfMessagesVisible',
    Namespace='AWS/SQS',
    Period=60,
    Statistic='Average',
    Threshold=100,
    ActionsEnabled=True,
    AlarmActions=[
        'arn:aws:sns:us-east-1:123456789012:queue-size-notification',
    ],
)

# create a new Auto Scaling group
autoscaling = boto3.client('autoscaling')

response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='my-app-instances',
    LaunchConfigurationName='my-launch-config',
    MinSize=1,
    MaxSize=20,
    DesiredCapacity=1,
    VPCZoneIdentifier='subnet-12345678',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'app-instance'
        },
    ]
)
