# 
# Author: Jose Lo Huang
# Creation Date: 23/11/2020
# Updates:
# 25/11/2020 - Create more functions
# 02/12/2020 - Add comments and the Error class
# 
# This code is to define the EBS class
# 

import boto3
import Error

class EBS:
    # 
    # The EBS class is able to execute all the following EBS related tasks:
    # 
    # 1. List all the volumes 
    # 2. Attach a volume to an instance 
    # 3. Detach a volume from an instance 
    # 4. Take a snapshot of a volume 
    # 5. Create a volume from a snapshot 
    # 

    def __init__ ( self, access_input, secret_input ):
        #
        # Each EBS class instantiation will create a resource and a client objects.
        # The client is used for the list_snapshots function.
        #
        self.ebs = boto3.resource("ec2",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        self.ebs_client = boto3.client("ec2",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        # This is a Error class invocation to print repetitive error messages
        self.error = Error.Error()
        

    def list_volumes ( self ):
        #
        # This function lists all the EBS volumes.
        # It will list all the EBS volumes and its statuses.
        # 
        try:
            # Get all volumes
            volumes = self.ebs.volumes.all()
            volumes_in_use = []
            # Print the columes in-use
            print("==================================================================")
            print("************************* IN-USE VOLUMES *************************")
            for vol in volumes:
                for attachments in vol.attachments:
                    volumes_in_use.append(vol.id)
                    print("Volume ID: "+vol.id
                          +" - Volume status: "+vol.state
                          +" - Instance: "+attachments['InstanceId']
                          +" - Device: "+attachments['Device'])
            # Print the available volumes 
            print("*********************** AVAILABLE VOLUMES ***********************")
            avail_volumes = []
            for vol in volumes:
                if vol.id in volumes_in_use:
                    pass
                else:
                    avail_volumes.append(vol.id)
                    print(vol.id)
        except:
            self.error.general_error("listing the EBS volumes")
        # Return a list with 2 lists: the volumes in-use and the available volumes
        return [volumes_in_use, avail_volumes]
        

    def attach_volume ( self ):
        #
        # This function attach an EBS volume to an EC2 instance.
        # It will request the following information from the user:
        # 1. Instance ID
        # 2. Volume ID
        # 3. Device Name
        # 
        try:
            # Get all the running and stopped instances
            instances_running = self.ebs.instances.filter(
                Filters=[{'Name': 'instance-state-name',
                          'Values': ['running', 'stopped']}])

            # Check how many running and stopped instances
            one_running = 0
            for instance in instances_running:
                one_running += 1

            # If there is no running or stopped instances, then return
            if (one_running == 0) :
                print("******************************************************************")
                print("NO INSTANCES IN RUNNING OR STOPPED STATE!")
                print("******************************************************************")
                return

            # Print the running and the stopped instances
            print("==================================================================")
            print("****************** RUNNING OR STOPPED INSTANCES ******************")
            instance_id_all = []
            while True:
                for instance in instances_running:
                    instance_id_all.append(instance.id)
                    print(instance.id)
                # Request instance id
                instance_id = input("Please insert the instance id you want use: ")
                # Check if instance id exists
                if instance_id in instance_id_all:
                    # Get the available volumes
                    volume_ids = (self.list_volumes())[1]
                    volume_id = input("Please insert the volume id you want use: ")
                    # Check if volume id exists
                    if volume_id in volume_ids:
                        # Check all the devices on the instance id
                        device_name = input("Please insert the device name you want use, for example ('/dev/sdf'): ")
                        try:
                            # Attach the volume
                            result = self.ebs_client.attach_volume (VolumeId=volume_id,
                                                                 InstanceId=instance_id,
                                                                 Device=device_name)
                            print("******************************************************************")
                            print("Attaching Volume")
                            print("******************************************************************")
                            break
                        except :
                            self.error.not_valid_value(device_name)
                            print("Check if the device name is already in use.")
                    else:
                        self.error.not_valid_value(volume_id)
                        print("Check if the volume id already exists.")
                else:
                    self.error.not_valid_value(instance_id)
        except:
            self.error.general_error("attaching the volume")
            

    def detach_volume ( self ):
        #
        # This function detach an EBS volume from an EC2 instance.
        # It will request the following information from the user:
        # 1. Volume ID
        # 
        try:
            while True:
                # Get the in-use volumes
                volume_ids = (self.list_volumes())[0]
                # Request the volume id
                volume_id = input("Please insert the volume id you want to detach : ")
                # Check if volume id exists
                if volume_id in volume_ids:
                    try:
                        # Detach volume
                        result = self.ebs_client.detach_volume (VolumeId=volume_id)
                        print("******************************************************************")
                        print("Detaching Volume")
                        print("******************************************************************")
                        break
                    except :
                        print("======> " + volume_id + " can't be detached or already detached.")
                        break
                else:
                    self.error.not_valid_value(volume_id)
        except:
            self.error.general_error("detaching the volume")


    def waiter ( self , snapshot_id ):
        #
        # This function will wait until a snapshot with snapshot id = 'snapshot_id' ends.
        # 
        snapshot_complete_waiter = self.ebs_client.get_waiter('snapshot_completed')
        try:
            # Wait until the snapshot is complete
            snapshot_complete_waiter.wait(SnapshotIds=[snapshot_id])
        except:
            print("The snapshot is taking more than 600 seconds.")
        print("******************************************************************")
        print("Snapshot completed. ")
        print("******************************************************************")
        

    def take_snapshot ( self ):
        #
        # This function take a snapshot of an EBS volume.
        # It will request the following information from the user:
        # 1. Volume ID
        # 
        try:
            while True:
                # Use the list_volumes() method to list all the volumes
                volume_ids = (self.list_volumes())
                # Request the volume id
                volume_id = input("Please insert the volume id of the volume that you want to take a snapshot : ")
                # Check if volume id is in-use (AWS docs mention an old issue with in-use volumes)
                if volume_id in volume_ids[0]:
                    try:
                        # Take the snapshot
                        result = self.ebs_client.create_snapshot (VolumeId=volume_id)
                        print("******************************************************************")
                        print("Taking a snapshot. ")
                        print("******************************************************************")
                        # Waiter section
                        snapshot_id = result['SnapshotId']
                        self.waiter(snapshot_id)
                        break
                    except :
                        # If the in-use volume snapshot fails 
                        print("======> " + volume_id + " is a root volume and is in use, you must stop the instance first.")
                        break
                # Check if volume id is not in-use
                elif volume_id in volume_ids[1]:
                    try:
                        result = self.ebs_client.create_snapshot (VolumeId=volume_id)
                        print("******************************************************************")
                        print("Taking a snapshot. ")
                        print("******************************************************************")
                        # Waiter section
                        snapshot_id = result['SnapshotId']
                        self.waiter(snapshot_id)
                        break
                    except :
                        print("======> " + volume_id + " can't be used to take snapshot. Check with AWS support.")
                        break
                else: 
                    self.error.not_valid_value(volume_id)
        except:
            self.error.general_error("taking the snapshot")


    def list_snapshots ( self ):
        #
        # This function lists all the EBS snapshots owned by this AWS account.
        # 
        try:
            # Get all the EBS snapshots (Owner AWS Account hidden)
            snapshots = self.ebs_client.describe_snapshots(OwnerIds=['************'])
            snapshot_dicts = snapshots['Snapshots']
            # Print the snapshots
            print("==================================================================")
            print("********************** AVAILABLE SNAPSHOTS ***********************")
            snap_ids = []
            for snap in snapshot_dicts:
                snap_ids.append(snap['SnapshotId'])
                print("Snapshot ID: "+snap['SnapshotId']
                          +" - Original Volume ID: "+snap['VolumeId'])
        except:
            self.error.general_error("listing the snapshots")
        return snap_ids


    def restore_snapshot ( self ):
        #
        # This function creates a volume from a snapshot.
        # It will request the following information from the user:
        # 1. Snapshot ID
        # 
        try:
            while True:
                # Use the function list_snapshots() to get the lsit of snapshots
                snapshot_ids = self.list_snapshots()
                # Request the snapshot id
                snapshot_id = input("Please insert the snapshot id of the volume that you want to restore : ")
                # Check if the snapshot id is on the available snapshots
                if snapshot_id in snapshot_ids:
                    try:
                        # Restore the snapshot 
                        result = self.ebs.create_volume (SnapshotId=snapshot_id,AvailabilityZone='eu-west-1a')
                        print("******************************************************************")
                        print("Restoring a snapshot to EBS volume. ")
                        print("******************************************************************")
                        break
                    except :
                        print("======> " + snapshot_id + " can't be restored. Please contact AWS support.")
                        break
                else: 
                    self.error.not_valid_value(snapshot_id)
        except:
            self.error.general_error("restoring the snapshots")




