import boto3
import time

# Initialize boto3 clients
ec2 = boto3.client('ec2')


def create_image(instance_id, name, tags):
    response = ec2.create_image(
        InstanceId=instance_id,
        Name=name,
        NoReboot=True,
        TagSpecifications=[
            {
                'ResourceType': 'image',
                'Tags': tags
            }
        ]
    )

    image_id = response['ImageId']
    print(f"Created image: {image_id}")
    return image_id


def create_multiple_images(instances_with_names, tags):
    results = []
    for instance_id, name in instances_with_names.items():
        result = create_image(instance_id, name, tags)
        results.append(result)
    return results

# Function to create a snapshot of a volume
def create_snapshot(volume_id, description, tags):
    response = ec2.create_snapshot(
        VolumeId=volume_id,
        Description = description,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': tags
            }
        ]
    )
    snapshot_id = response['SnapshotId']
    print(f"Created snapshot: {snapshot_id}")
    return snapshot_id

def create_multiple_snapshot(volume_id, tags):
    results = []
    for id, name in volume_id.items():
        result = create_image(id, name, tags)
        results.append(result)
    return results

# Function to copy a snapshot
def copy_snapshot(source_snapshot_id, source_region, target_region):
    response = ec2.copy_snapshot(
        SourceSnapshotId=source_snapshot_id,
        SourceRegion=source_region,
        DestinationRegion=target_region,
        Description="Copy of " + source_snapshot_id
    )
    copy_snapshot_id = response['SnapshotId']
    print(f"Copied snapshot: {copy_snapshot_id}")
    return copy_snapshot_id

def copy_multiple_snapshot(source_snapshot_id, source_region, target_region):
    time.sleep(300)
    results = []
    for id in source_snapshot_id:
        result = copy_snapshot(id, source_region, target_region)
        results.append(result)
    return results

# Function to share a snapshot with another account
def modify_snapshot_attribute(snapshot_id, account_id):
    ec2.modify_snapshot_attribute(
        SnapshotId=snapshot_id,
        Attribute='createVolumePermission',
        OperationType='add',
        UserIds=[account_id]
    )
    print(f"Shared snapshot {snapshot_id} with account {account_id}")

def modify_multiple_snapshot_attribute(snapshot_id, account_id):
    time.sleep(300)
    results = []
    for id in snapshot_id:
        result = modify_snapshot_attribute(id, account_id)
        results.append(result)
    return results


#  Make the AMI public or share with specific accounts
def modify_image_attribute(image_id, account_id):
    
    ec2.modify_image_attribute(
        ImageId=image_id,
        Attribute='launchPermission',
        OperationType='add',
        UserIds=[account_id]
    )
    print(f"Shared AMI {image_id} with account {account_id}")
    
def modify_multiple_image_attribute(image_id, account_id):
    time.sleep(300)
    results = []
    for image_id in image_id:
        result = modify_image_attribute(image_id, account_id)
        results.append(result)
    return results    

if __name__ == "__main__":
    # instance_id and volume_id need to be in dictionary key: instance ID, value: name of instance(depend on your preferance)
    instance_id = {}
    volume_id = {}
    source_region = ''
    target_region = ''
    account_id =  ''
    tags = [
        {'Key': '', 'Value': ''}
    ]
    
    image_id = create_multiple_images(instance_id, tags)
    
    snapshot_id = create_multiple_snapshot(volume_id, tags)
    copy_snapshot_id = copy_multiple_snapshot(snapshot_id, source_region, target_region)
    
    modify_multiple_image_attribute(image_id, account_id)
    modify_multiple_snapshot_attribute(copy_snapshot_id, account_id)