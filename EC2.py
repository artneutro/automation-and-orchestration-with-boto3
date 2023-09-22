# 
# Author: Jose Lo Huang
# Creation Date: 20/11/2020
# Updates:
# 23/11/2020 - Create more functions
# 02/12/2020 - Add comments and the Error class
# 
# This code is to define the EC2 class
# 

import boto3
import Error

class EC2:
    # 
    # The EC2 class is able to execute all the following EC2 tasks:
    # 
    # 1. List all the instances 
    # 2. Start an instance 
    # 3. Stop an instance 
    # 4. Create an AMI from instance 
    # 5. Launch a new instance
    # 

    def __init__ ( self, access_input, secret_input ):
        #
        # Each EC2 class instantiation will create a resource and a client objects.
        # The client is used for the AMI creation and the resource object for the other functions.
        #
        self.ec2 = boto3.resource("ec2",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        self.ec2_client = boto3.client("ec2",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        # This is a Error class invocation to print repetitive error messages
        self.error = Error.Error()


    def list_instances( self ):
        #
        # This function lists all the EC2 instances.
        # It will list all the running instances first and then,
        # all the other instances in different states.
        # 
        try:
            all_instances = []
            # Get all the running instances
            instances_running = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name',
                          'Values': ['running']}])
            print("==================================================================")
            print("*********************** RUNNING INSTANCES ************************")
            # Print all the running instances
            for instance in instances_running:
                all_instances.append(instance.id)
                print("State : " + instance.state['Name'],
                      "- Instance id: " + instance.id,
                      "- Type: " + instance.instance_type,
                      "- Region: eu-west-1",
                      "- Launch time: " + str(instance.launch_time))
            # Get all the non-runing instances
            instances_not_running = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name',
                          'Values': ['pending' , 'shutting-down' , 'terminated' , 'stopping' , 'stopped']}])
            print("********************* NOT RUNNING INSTANCES **********************")
            # Print all the non-running instances
            for instance in instances_not_running:
                all_instances.append(instance.id)
                print("State : " + instance.state['Name'],
                      "- AMI id: " + instance.id,
                      "- Type: " + instance.instance_type,
                      "- Region: eu-west-1",
                      "- Launch time: " + str(instance.launch_time))
            return all_instances
        except:
            self.error.general_error("listing the EC2 instances")


    def start_instance( self ):
        #
        # This function request an instance ID and starts it.
        # If there aren't stopped EC2 instances, it will print a message and return.
        # 
        try:
            # Get all the stopped EC2 instances
            instances_stopped = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name',
                          'Values': ['stopped']}])

            # Check how many are stopped
            one_stopped = 0
            for instance in instances_stopped:
                one_stopped += 1

            # If there is no stopped instances, then return
            if (one_stopped == 0) :
                print("******************************************************************")
                print("NO INSTANCES IN STOPPED STATE!")
                print("******************************************************************")
                return

            # List the stopped instances
            print("==================================================================")
            print("*********************** STOPPED INSTANCES ************************")
            instance_id_all = []
            while True:
                for instance in instances_stopped:
                    instance_id_all.append(instance.id)
                    print(instance.id)
                # Request the instance id
                instance_id = input("Please insert the instance id you want start: ")
                if instance_id in instance_id_all:
                    # Start the EC2 instance
                    self.ec2.instances.filter(InstanceIds = [instance_id]).start()
                    print("******************************************************************")
                    print("Starting instance: "+str(instance_id))
                    print("******************************************************************")
                    break
                else:
                    self.error.not_valid_value(instance_id)
                    
        except:
            self.error.general_error("starting the EC2 instance")


    def stop_instance( self ):
        #
        # This function request an instance ID and stops it.
        # If there aren't running EC2 instances, it will print a message and return.
        # 
        try:
            # Get the running instances
            instances_running = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name',
                          'Values': ['running']}])

            # Check how many are running
            one_running = 0
            for instance in instances_running:
                one_running += 1

            # If there is no started instances, then return            
            if (one_running == 0) :
                print("******************************************************************")
                print("NO INSTANCES IN RUNNING STATE!")
                print("******************************************************************")
                return

            # List the running instances
            print("==================================================================")
            print("*********************** RUNNING INSTANCES ************************")
            instance_id_all = []
            while True:
                for instance in instances_running:
                    instance_id_all.append(instance.id)
                    print(instance.id)
                # Request the instance id
                instance_id = input("Please insert the instance id you want stop: ")
                if instance_id in instance_id_all:
                    # Stop the EC2 instance
                    self.ec2.instances.filter(InstanceIds = [instance_id]).stop()
                    print("******************************************************************")
                    print("Stopping instance: "+str(instance_id))
                    print("******************************************************************")
                    break
                else:
                    self.error.not_valid_value(instance_id)
                    
        except:
            self.error.general_error("stopping the instance")


    def create_ami( self ):
        #
        # This function request an instance ID and a name and creates an EC2 AMI of the instance.
        # If there aren't running or stopped EC2 instances, it will print a message and return.
        # 
        try:
            # According to AWS docs, we can create AMIs of running or stopped instances only
            instances_rs = self.ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name',
                          'Values': ['running' , 'stopped']}])

            # Check how many are running or stopped
            one_rs = 0
            for instance in instances_rs:
                one_rs += 1

            # If there is no running or stopped instances, then return
            if (one_rs == 0) :
                print("******************************************************************")
                print("NO INSTANCES IN RUNNING OR STOPPED STATE!")
                print("******************************************************************")
                return

            # List the running and stopped instances
            print("==================================================================")
            print("***************** RUNNING AND STOPPED INSTANCES ******************")
            instance_id_all = []
            while True:
                for instance in instances_rs:
                    instance_id_all.append(instance.id)
                    print(instance.id)
                # Request the instance id
                instance_id = input("Please insert the instance id to create the AMI: ")
                if instance_id in instance_id_all:
                    # Request the AMI name
                    ami_name = input("Please insert the new AMI name: ")
                    # Create the EC2 AMI
                    self.ec2_client.create_image(InstanceId=instance.id, NoReboot=True, Name=ami_name)
                    print("******************************************************************")
                    print("Creating AMI of: "+str(instance_id)+" with name : "+ami_name)
                    print("******************************************************************")
                    break
                else:
                    self.error.not_valid_value(instance_id)
                    
        except:
            self.error.general_error("creating the AMI")


    def create_instance_linux( self ):
        #
        # This function creates an EC2 Linux instance using a default AMI and instance type.
        # 
        try:
            self.ec2.create_instances(ImageId='ami-014ce76919b528bff',
                                      MinCount=1,
                                      MaxCount=1,
                                      InstanceType='t2.micro',
                                      Placement={'AvailabilityZone':'eu-west-1a'})
            print("******************************************************************")
            print("Creating instance.")
            print("******************************************************************")
        except:
            self.error.general_error("creating the EC2 instance")


    def create_instance_windows( self ):
        #
        # This function creates an EC2 Windows instance using a default AMI and instance type.
        # 
        try:
            self.ec2.create_instances(ImageId='ami-065a15cef040336bf',
                                      MinCount=1,
                                      MaxCount=1,
                                      InstanceType='t2.micro',
                                      Placement={'AvailabilityZone':'eu-west-1a'})
            print("******************************************************************")
            print("Creating instance.")
            print("******************************************************************")
        except:
            self.error.general_error("creating the EC2 instance")
            
