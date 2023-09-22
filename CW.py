# 
# Author: Jose Lo Huang
# Creation Date: 26/11/2020
# Updates:
# 03/11/2020 - Add comments and the Error class
# 
# This code is to define the CW class
#

import boto3
import datetime
import EC2
import Error

class CW:
    # 
    # The CW class is able to execute all the following CW related tasks:
    # 
    # 1. Print the CPU-Utilization and Network-Out metrics for an instance
    # 2. Set CPU-Utilization alarm on instance and send notification via SNS
    # 

    def __init__ (self, access_input, secret_input):
        #
        # Each CW class instantiation will create a resource and a client objects.
        # The client is used for most functions and the resource is there for future purposes.
        #
        self.access_input = access_input
        self.secret_input = secret_input
        self.cw = boto3.resource("cloudwatch",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        self.cw_client = boto3.client("cloudwatch",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        # This is a Error class invocation to print repetitive error messages
        self.error = Error.Error()

        
    def show_metrics ( self ):
        #
        # This function will show the CPU-Utilization and Network-Out metrics for 
        # an EC2 instance chosen by the user.
        # It request the following inputs from user:
        # 1. EC2 instance id
        # 
        try:
            # Create an EC2 class instantiation
            ec2 = EC2.EC2(self.access_input, self.secret_input)
            while True:
                # Show all EC2 instances
                all_instances = ec2.list_instances()
                # Request the instance id
                instance_id = input("Please insert the EC2 instance ID you want check: ")
                # Check if instance exists
                if instance_id in all_instances:
                    try:
                        # Print the 2 metrics
                        print("==================================================================")
                        print("***************** AVERAGE IN THE LAST 10 MINUTES *****************")
                        # CPUUtilization
                        cpu = self.cw_client.get_metric_statistics(
                                Namespace='AWS/EC2',
                                MetricName='CPUUtilization',
                                Dimensions=[
                                    {
                                    'Name': 'InstanceId',
                                    'Value': instance_id
                                    },
                                ],
                                StartTime=datetime.datetime.now() - datetime.timedelta(minutes=10),
                                EndTime=datetime.datetime.now(),
                                Period=5,
                                Statistics=[
                                    'Average',
                                ],
                                Unit='Percent'
                            )
                        print("CPU Utilization Average = " + str(cpu['Datapoints'][0]['Average']))
                        # NetworkOut
                        network = self.cw_client.get_metric_statistics(
                                Namespace='AWS/EC2',
                                MetricName='NetworkOut',
                                Dimensions=[
                                    {
                                    'Name': 'InstanceId',
                                    'Value': instance_id
                                    },
                                ],
                                StartTime=datetime.datetime.now() - datetime.timedelta(minutes=10),
                                EndTime=datetime.datetime.now(),
                                Period=5,
                                Statistics=[
                                    'Average',
                                ]
                            )
                        print("Network Out Average = " + str(network['Datapoints'][0]['Average']))
                        return
                    except :
                        print("======> There is a problem and the metrics can't be readed, the EC2")
                        print(" instance is stopped or you don't have permissions.")
                        break
                else:
                    self.error.not_valid_value(instance_id)
        except:
            self.error.general_error()


    def is_letter( self , char ):
        #
        # Check if a char is a lowercase letter
        # It returns True or False accordingly
        # 
        return (97<=ord(char)<=122)


    def is_number_or_letter( self , char ):
        #
        # Check if a char is number or letter
        # It returns True or False accordingly
        # 
        return (48<=ord(char)<=57 or 65<=ord(char)<=90 or 97<=ord(char)<=122)


    def check_email( self , email ):
        #
        # Check if an input has an email structure.
        # According to web references, the minimum are
        # 5 characters: a@a.a
        # It returns True or False accordingly
        # 
        have_at = False
        have_domain = False
        # Email can't be less than 5 chars, must start with character or number and end with character
        if (len(email) < 5) or (not self.is_number_or_letter(email[0])) or (not self.is_letter(email[len(email)-1])):
            return False
        for char in email:
            if char == '@':
                if (have_at):
                    return False
                else:
                    have_at = True
            elif char == ' ':
                return False
            elif char == '.' and not have_at:
                pass
            elif char == '.' and have_at:
                have_domain = True
            elif char == '-' or char == '_':
                pass
            elif self.is_number_or_letter(char):
                pass
            else:
                return False
        if have_at and have_domain:
            return True
            
            
    def set_alarm ( self ):
        #
        # This function set a CloudWatch alarm such when the CPUUtilization of
        # an EC2 instance is below 28% during a period, it will be triggered
        # and send an email.
        # It will request:
        # 1. The EC2 instance id
        # 2. The email address
        # 
        try:
            ec2 = EC2.EC2(self.access_input, self.secret_input)
            while True:
                # Show all EC2 instances
                all_instances = ec2.list_instances()
                # Request the EC2 instance id
                instance_id = input("Please insert the EC2 instance ID that you want to set the alarm: ")
                # Check if instance exists
                if instance_id in all_instances:
                    try:
                        print("==================================================================")
                        print("***************** THIS WILL SET AN ALARM TO THE  *****************")
                        print("*************** EC2 INSTANCE WHEN CPU UTILIZATION  ***************")
                        print("*************** IS LESS THAN 28% DURING 60 SECONDS ***************")
                        while True:
                            # Request the email address
                            email = input("Please insert your email address where the alarm will be sent: ")
                            if self.check_email(email.lower()):
                                break
                            else:
                                print("The email address is not a valid email.")
                        # Create the subscription to the topic
                        sns_client = boto3.client('sns',
                                                  aws_access_key_id=self.access_input,
                                                  aws_secret_access_key=self.secret_input)
                        response = sns_client.subscribe(
                            TopicArn='arn:aws:sns:eu-west-1:************:CPU_Utilization',
                            Protocol='email',
                            Endpoint=email
                        )
                        # Create the alarm 
                        self.cw_client.put_metric_alarm(
                            AlarmName=instance_id+"_CPU_Utilization",
                            ComparisonOperator='LessThanThreshold',
                            EvaluationPeriods=1,
                            MetricName='CPUUtilization',
                            Namespace='AWS/EC2',
                            Period=60,
                            Statistic='Average',
                            Threshold=28.0,
                            ActionsEnabled=True,
                            AlarmActions=['arn:aws:sns:eu-west-1:************:CPU_Utilization'],
                            AlarmDescription='Alarm when server CPU is lower than 28%',
                            Dimensions=[
                                {
                                  'Name': 'InstanceId',
                                  'Value': 'INSTANCE_ID'
                                },
                            ],
                            Unit='Seconds'
                        )
                        print("*********** An alarm was set to your email: "+email+" ************")
                        print("****** Kindly check your email and accept the subscription *******")                      
                        return
                    except :
                        print("======> There is a problem with the CW metrics or SNS service")
                        print(" or you don't have permissions.")
                        break
                else:
                    self.error.not_valid_value(instance_id)
        except:
            self.error.general_error()






