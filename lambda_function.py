import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    #Get the action(start or stop) from the EventBridge trigger
    action = event.get('action')

    #Get the IDs of the instances
    instances = ec2.describe_instances()

    instance_ids = []
    # Loop through reservations and instances to collect Instance IDs
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    # If no instances found, exit the function
    if not instance_ids:
        print('No instances found')
        return

    # Start instances if action is 'start' or
    # Stop instances if action is 'stop'
    if  action == 'start':
        ec2.start_instances(InstanceIds=instance_ids)
        print(f"The instances started {instance_ids}")
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"The instances stopped {instance_ids}")
    else:
        print("Invalid action provided in event.")
    return {
        'statusCode': 200,
        'body': f"Action {action} executed on instances {instance_ids}"
    }

