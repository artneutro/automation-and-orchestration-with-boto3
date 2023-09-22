Republic of Ireland
Department of Computer Science
Student: Jose Lo Huang

##################################
1. Introduction
##################################

This code is designed to manage some AWS services in a simple and easy way.

This is the version 1, which includes the following AWS services:

* Elastic Compute Cloud (EC2)
* Elastic Block Storage (EBS)
* Simple Storagee Service (S3)
* CloudWatch (CW)

Also includes a beta version of the Relational Database Service (RDS) with
short examples.

##################################
2. Code
##################################

The code included on this package is as follows:

* AWS-manager.py = Manage the main program and login process.
* Menus.py = Includes all the menus and submenus.
* EC2.py = Define the EC2 class and functions.
* EBS.py = Define the EBS class and functions.
* S3.py = Define the S3 class and functions.
* CW.py = Define the CW class and functions.
* RDS.py = Define the RDS class and functions. Currently in beta version.
* Error.py = Define the Error class and functions.
* passwd.txt = The file with the AWS programmatic access credentials.

Note: All the files must be on the same directory. 

2.1. How to Run 

The code was tested on Linux and Mac with Python 3.8.5. 

./AWS-manager.py

2.2. Components and classes dependencies tree

+- AWS-manager +- Menu +- EC2
               |       +- EBS
               |       +- S3
               |       +- CW
               |       +- Error 
               +- passwd.txt
+- RDS

2.3. Menus and submenus

2.3.1. The main menu

AWS MANAGER V2.0.
1. EC2
2. EBS
3. S3
4. CW
5. Exit

2.3.2. The EC2 submenu tasks

EC2 Menu : 
1. List all the instances 
2. Start an instance  
3. Stop an instance 
4. Create an AMI from instance 
5. Launch a new instance 

2.3.3. The EBS submenu tasks

EBS Menu : 
1. List all the volumes 
2. Attach a volume to an instance 
3. Detach a volume from an instance 
4. Take a snapshot of a volume 
5. Create a volume from a snapshot 

2.3.4. The S3 submenu tasks

S3 Menu : 
1. List all the buckets 
2. List all the objects in a bucket 
3. Upload an object 
4. Download an object  
5. Delete an object  

2.3.5. The CW submenu tasks

CW Menu : 
1. Display 2 performance metrics 
2. Set an alarm 

##################################
3. Conclusion
##################################

After run this code, the user can manage the AWS services in an easy and
efficient way. Even easier than the AWS CLI, where we need to remember a
large amount of parameters.

##################################
4. References 
##################################

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-examples.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html








