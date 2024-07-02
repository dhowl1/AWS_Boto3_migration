import boto3

# Initialize boto3 clients
ec2 = boto3.client('ec2')

def launch_instance(image_id, instance_type, key_name, security_group_ids, subnet_id, tags):
    response = ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        SubnetId=subnet_id,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags
            }
        ]
    )


    instance_id = response['Instances'][0]['InstanceId']
    print(f"Launched instance: {instance_id}")
    return instance_id

# Example usage in the target account
if __name__ == "__main__":
    #open txt, then read everything in there which is IAM ID
    image_id = '' 
    instance_type = ''
    key_name = ''
    security_group_ids = ['']
    subnet_id = ''
    tags = [
        {'Key': '', 'Value': ''}
    ]
    
    new_instance_id = launch_instance(image_id, instance_type, key_name, security_group_ids, subnet_id, tags)