#!/usr/bin/env python3
# 
# Author: Jose Lo Huang
# Creation Date: 27/11/2020
# Updates: None
# 

#
# Description of RDS:
# 
# RDS (Relational Database Service) is the AWS service which offers
# Relational-based databases as a service (DBaaS). The engine options are:
# 1. Oracle
# 2. SQL Server
# 3. MySQL
# 4. PostgreSQL
# 5. MariaDB
# 6. Aurora
# 6.1. Aurora MySQL
# 6.2. Aurora PostgreSQL
# 6.3. Aurora MySQL Serverless
# 6.4. Aurora PostgreSQL Serverless
# 

#
# Detailed Example of this AWS service usage with Boto3.
# List all RDS instances
# 

import boto3

# Connect to AWS RDS using the credentials for programmatic access (AWS credentials hidden)
rds = boto3.client('rds',
                   aws_access_key_id='AKIA****************',
                   aws_secret_access_key='**********************************')
# Get the configuration of all RDS instances
rds_instances = rds.describe_db_instances()
# Loop over all the RDS instances and print the configuration
for db in rds_instances['DBInstances']:
    db_instance_name = db['DBInstanceIdentifier']
    db_type = db['DBInstanceClass']
    db_storage = db['AllocatedStorage']
    db_engine = db['Engine']
    print ("RDS Instance Name: "+db_instance_name,
           "Instance Type: "+db_type,
           "Storage Size: "+str(db_storage),
           "DB Engine: "+db_engine)

#
# Example short functions (4)
#

def create_instance(rds_client):
    # 
    # This function creates an RDS instance.
    # It will receive as input:
    # 1. An RDS client instantiation
    #
    try:
        rds_client.create_db_instance(DBInstanceIdentifier='test-db',
                                                  DBInstanceClass='db.r5.large',
                                                  Engine='mysql',
                                                  MasterUsername='master',
                                                  MasterUserPassword='welcome1',
                                                  AllocatedStorage=20)
        print("Creating")
    except:
        print ("The DB already exists or you don't have permissions. ")

# Tested with: 
#create_instance(rds)

def stop_instance(rds_client):
    # 
    # This function stop an RDS instance.
    # It will receive as input:
    # 1. An RDS client instantiation
    #
    try:
        rds_client.stop_db_instance(DBInstanceIdentifier='test-db')
        print("Stopping")
    except:
        print ("The DB is not running, doesn't exists or you don't have permissions. ")

# Tested with: 
#stop_instance(rds)

def start_instance(rds_client):
    # 
    # This function start an RDS instance.
    # It will receive as input:
    # 1. An RDS client instantiation
    #
    try:
        rds_client.start_db_instance(DBInstanceIdentifier='test-db')
        print("Starting")
    except:
        print ("The DB is running, doesn't exists or you don't have permissions. ")

# Tested with: 
#start_instance(rds)

def delete_instance(rds_client):
    # 
    # This function deletes an RDS instance.
    # It will receive as input:
    # 1. An RDS client instantiation
    #
    try:
        rds_client.delete_db_instance(DBInstanceIdentifier='test-db',
                                      SkipFinalSnapshot=True,
                                      DeleteAutomatedBackups=True)
        print("Deleting")
    except:
        print ("The DB doesn't exists or you don't have permissions. ")

# Tested with: 
#delete_instance(rds)









