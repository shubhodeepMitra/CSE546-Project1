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

# Set up the client and resource for EC2 and SQS
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
sqs_client = boto3.client('sqs')
sqs_resource = boto3.resource('sqs')

# Set up the autoscaling group
asg_client = boto3.client('autoscaling')
asg_group_name = 'my-autoscaling-group'
min_instances = 1
max_instances = 20

# Set up the SQS queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
queue = sqs_resource.Queue(queue_url)

# Set up the CloudWatch alarms
alarm_name = 'my-alarm'
metric_name = 'ApproximateNumberOfMessagesVisible'
namespace = 'AWS/SQS'
comparison_operator = 'GreaterThanThreshold'
threshold = 5
evaluation_periods = 1
period = 60
actions_enabled = True
autoscaling_policy_name = 'my-scaling-policy'

"""
Requirement:
The max scale up number of instances should be 20. If the requests are less than 20, then the number of ec2 instances should be almost the number of requests in the queue.
However, if the requests are more than 20, then the auto scaling should maintain max count of instances to be 20, it should not exceed that threshold.
"""
# Create the CloudWatch alarm and set up the autoscaling policy
def create_alarm_and_policy():
    response = None
    try:
        response = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])
    except:
        pass
    if response and 'Attributes' in response:
        queue_size = int(response['Attributes']['ApproximateNumberOfMessages'])
        print(f"Queue size: {queue_size}")
        if queue_size > 0:
            response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_group_name])
            if response and 'AutoScalingGroups' in response and len(response['AutoScalingGroups']) > 0:
                current_instances = len(response['AutoScalingGroups'][0]['Instances'])
                print(f"Current instances: {current_instances}")
                desired_instances = min(queue_size, max_instances) if queue_size <= max_instances else max_instances
                print(f"Desired instances: {desired_instances}")
                if desired_instances != current_instances:
                    asg_client.set_desired_capacity(AutoScalingGroupName=asg_group_name, DesiredCapacity=desired_instances)
                    print(f"Set desired capacity to {desired_instances}")
            if queue_size > threshold:
                response = asg_client.describe_policies(AutoScalingGroupName=asg_group_name, PolicyNames=[autoscaling_policy_name])
                if response and 'ScalingPolicies' in response and len(response['ScalingPolicies']) > 0:
                    asg_client.execute_policy(AutoScalingGroupName=asg_group_name, PolicyName=autoscaling_policy_name)
                    print(f"Executed scaling policy: {autoscaling_policy_name}")
                else:
                    scaling_policy = asg_client.put_scaling_policy(AutoScalingGroupName=asg_group_name, PolicyName=autoscaling_policy_name,
                                                                     PolicyType='SimpleScaling', AdjustmentType='ChangeInCapacity',
                                                                     ScalingAdjustment=1, Cooldown=60, MinAdjustmentMagnitude=1)
                    print(f"Created scaling policy: {autoscaling_policy_name}")
                    asg_client.put_metric_alarm(AlarmName=alarm_name, ComparisonOperator=comparison_operator,
                                                EvaluationPeriods=evaluation_periods, MetricName=metric_name, Namespace=namespace,
                                                Period=period, Statistic='Average', Threshold=threshold,
                                                ActionsEnabled=actions_enabled, AlarmActions=[scaling_policy['PolicyARN']])
                    print(f"Created alarm: {alarm_name}")

create_alarm_and_policy()
