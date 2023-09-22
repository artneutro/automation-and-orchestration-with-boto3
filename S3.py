# 
# Author: Jose Lo Huang
# Creation Date: 25/11/2020
# Updates:
# 26/11/2020 - Add last 2 functions
# 03/12/2020 - Add comments and the Error class
# 
# This code is to define the S3 class
# 

import boto3
import Error

class S3:
    # 
    # The S3 class is able to execute all the following S3 related tasks:
    # 
    # 1. List all the buckets 
    # 2. List all the objects in a bucket 
    # 3. Upload an object 
    # 4. Download an object 
    # 5. Delete an object 
    # 

    def __init__ (self, access_input, secret_input):
        #
        # Each S3 class instantiation will create a resource and a client objects.
        # The client is used for the delete_object function and the resource
        # object for the other functions.
        #
        self.s3 = boto3.resource("s3",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")

        self.s3_client = boto3.client("s3",
                             aws_access_key_id=access_input,
                             aws_secret_access_key=secret_input,
                             region_name="eu-west-1")
        # This is a Error class invocation to print repetitive error messages
        self.error = Error.Error()


    def list_buckets ( self ):
        #
        # This function will list all the buckets of this user.
        # It returns a list with all the bucket names.
        # 
        try:
            print("==================================================================")
            print("*************************** S3 BUCKETS ***************************")
            buckets = []
            for bucket in self.s3.buckets.all():
                buckets.append(bucket.name)
                print(bucket.name)
            print()
        except:
            self.error.general_error("listing the S3 buckets")
        return buckets
        

    def list_objects ( self ):
        #
        # This function will list all the objects inside a bucket.
        # It will request the following from user:
        # 1. Bucket Name
        # 
        try:
            while True:
                # Show all buckets
                buckets = self.list_buckets()
                objects = []
                # Request the bucket name
                bucket_id = input("Please insert the bucket you want use: ")
                # Check if the bucket exists
                if bucket_id in buckets:
                    try:
                        # Get all the objects on the bucket
                        object_list = self.s3.Bucket(bucket_id).objects.all()
                        # Print all the objects of the bucket
                        print("==================================================================")
                        print("************************* BUCKET OBJECTS *************************")
                        for obj in object_list:
                            objects.append(obj.key)
                            print(obj.key)
                        # Return all the resources for processing on other functions.
                        # The list of bucket names, the chosen bucket_id
                        # and the list of objects inside this bucket_id
                        return [buckets, bucket_id, objects]
                    except :
                        print("======> Bucket " + bucket_id + " can't be readed or you don't have permissions.")
                        break
                else:
                    self.error.not_valid_value(bucket_id)
        except:
            self.error.general_error("listing the objects inside the bucket")


    def upload_object ( self ):
        #
        # This function will upload an object from the local machine to the bucket.
        # It will request the following from user:
        # 1. Bucket Name
        # 2. File Name
        # 
        try:
            while True:
                # Show all buckets
                buckets = self.list_buckets()
                # Request the bucket name
                bucket_id = input("Please insert the bucket you want use: ")
                # Check if bucket exists
                if bucket_id in buckets:
                    try:
                        while True:
                            # Request the file to upload
                            file_name = input("Please insert the name of your file to upload: ")
                            try:
                                # Upload the file
                                self.s3.meta.client.upload_file(file_name, bucket_id, file_name)
                                print("************************** Uploading ***************************")
                                return
                            except:
                                print("======> The file " + file_name + " can't be readed or you don't have permissions.")
                                break
                    except :
                        print("======> Bucket " + bucket_id + " can't be readed or you don't have permissions.")
                        break
                else:
                    self.error.not_valid_value(bucket_id)
        except:
            self.error.general_error("uploading the object")


    def download_object ( self ):
        #
        # This function will download an object from the bucket to the local machine.
        # It will request the following from user:
        # 1. Bucket Name
        # 2. Object Name
        # 
        try:
            while True:
                # Show all buckets and request the bucket name
                bucket_and_objects = self.list_objects()
                buckets = bucket_and_objects[0]
                bucket_id = bucket_and_objects[1]
                # Show the objects in the bucket
                if bucket_id in buckets:
                    objects = bucket_and_objects[2]
                    # Request the object to download
                    file_name = input("Please insert the name of the object to download: ")
                    if file_name in objects:
                        try:
                            # Download the object
                            self.s3.Bucket(bucket_id).download_file(file_name, file_name)
                            print("************************** Downloading ***************************")
                            return
                        except:
                            print("======> The object " + file_name + " doesn't exists or you don't have permissions.")
                            break
                    else:
                        print("======> The object " + file_name + " doesn't exists on the bucket.")
                else:
                    self.error.not_valid_value(bucket_id)
        except:
            self.error.general_error("downloading the object")


    def delete_object ( self ):
        #
        # This function will delete an object from the bucket.
        # It will request the following from user:
        # 1. Bucket Name
        # 2. Object Name
        # 
        try:
            while True:
                # Show all buckets and request the bucket name
                bucket_and_objects = self.list_objects()
                buckets = bucket_and_objects[0]
                bucket_id = bucket_and_objects[1]
                # Show the objects in the bucket
                if bucket_id in buckets:
                    objects = bucket_and_objects[2]
                    # Request the object to delete
                    file_name = input("Please insert the name of the object to delete: ")
                    if file_name in objects:
                        try:
                            # Delete the object
                            self.s3_client.delete_object(Bucket=bucket_id, Key=file_name)
                            print("*************************** Deleting *****************************")
                            return
                        except:
                            print("======> The object " + file_name + " doesn't exists or you don't have permissions.")
                            break
                    else:
                        print("======> The object " + file_name + " doesn't exists on the bucket.")
                else:
                    self.error.not_valid_value(bucket_id)
        except:
            self.error.general_error("deleting the object")





