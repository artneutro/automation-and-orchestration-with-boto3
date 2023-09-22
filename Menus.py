# 
# Author: Jose Lo Huang
# Creation Date: 20/11/2020
# Updates:
# 23/11/2020 - Add the getpass package to hide the password in Python.
# 01/12/2020 - Minor fixes and add comments for better read.
# 
# This code is to maintain all the management menus and submenus in the same place.
# From this code, the specific AWS tasks are triggered using the EC2, EBS, S3 and CW classes.
# 

import EC2
import EBS
import S3
import CW
import Error

error = Error.Error()

def main_menu ():
    # 
    # Main Menu:
    # This function shows the main menu and request the user option.
    # 
    print("==================================================================")
    print("AWS MANAGER V2.0.")
    print("1. EC2")
    print("2. EBS")
    print("3. S3")
    print("4. CW")
    print("5. Exit")
    print("==================================================================")
    option = input("Please insert the number of the service you want to manage : ")
    return option

def os_type_menu ():
    #
    while True:
        print("==================================================================")
        print("Choose your OS type : ")
        print("1. Linux ")
        print("2. Windows ") 
        print("==================================================================")    
        option = input("Please insert the number of your option : ")
        if (option == "1"):
            return True
        elif (option == "2"):
            return False
        else:
            print("======> " + option + " is not a valid value.")
            print("Please choose a valid value.")


def ec2_menu (keys):
    # 
    # EC2 Menu:
    # This function shows the EC2 menu and request the user option.
    # It will create an instance of the EC2 class and invoke the
    # EC2 function/procedure requested by the user.
    # 
    ec2 = EC2.EC2(keys[1],keys[2])
    while True:
        print("==================================================================")
        print("EC2 Menu : ")
        print("1. List all the instances ")
        print("2. Start an instance ") 
        print("3. Stop an instance ") 
        print("4. Create an AMI from instance ") 
        print("5. Launch a new instance ") 
        print("6. Go to the main menu ") 
        print("7. Exit program ") 
        print("==================================================================")    
        option = input("Please insert the number of your option : ")
        print()
        if (option == "1"):
            # 1. List all the instances
            ec2.list_instances()
        elif (option == "2"):
            # 2. Start an instance
            ec2.start_instance()
        elif (option == "3"):
            # 3. Stop an instance
            ec2.stop_instance()
        elif (option == "4"):
            # 4. Create an AMI from instance
            ec2.create_ami()
        elif (option == "5"):
            # 5. Launch a new instance
            os_type = os_type_menu()
            if (os_type) :
                # Linux
                ec2.create_instance_linux()
            else :
                # Windows
                ec2.create_instance_windows()
        elif (option == "6"):
            del ec2
            return 0
        elif (option == "7"):
            del ec2
            return 1
        else:
            error.not_valid_value(option)
        print()


def ebs_menu (keys):
    # 
    # EBS Menu:
    # This function shows the EBS menu and request the user option.
    # It will create an instance of the EBS class and invoke the
    # EBS function/procedure requested by the user.
    # 
    ebs = EBS.EBS(keys[1],keys[2])
    while True:
        print("==================================================================")
        print("EBS Menu : ")
        print("1. List all the volumes ")
        print("2. Attach a volume to an instance ") 
        print("3. Detach a volume from an instance ") 
        print("4. Take a snapshot of a volume ") 
        print("5. Create a volume from a snapshot ") 
        print("6. Go to the main menu") 
        print("7. Exit program") 
        print("==================================================================")    
        option = input("Please insert the number of your option : ")
        print()
        if (option == "1"):
            # 1. List all the volumes
            ebs.list_volumes()
        elif (option == "2"):
            # 2. Attach a volume to an instance
            ebs.attach_volume()
        elif (option == "3"):
            # 3. Detach a volume from an instance
            ebs.detach_volume()
        elif (option == "4"):
            # 4. Take a snapshot of a volume
            ebs.take_snapshot()
        elif (option == "5"):
            # 5. Create a volume from a snapshot
            ebs.restore_snapshot()
        elif (option == "6"):
            del ebs
            return 0
        elif (option == "7"):
            del ebs
            return 1
        else:
            error.not_valid_value(option)
        print()
            

def s3_menu (keys):
    # 
    # S3 Menu:
    # This function shows the S3 menu and request the user option.
    # It will create an instance of the S3 class and invoke the
    # S3 function/procedure requested by the user.
    # 
    s3 = S3.S3(keys[1],keys[2])
    while True:
        print("==================================================================")
        print("S3 Menu : ")
        print("1. List all the buckets ")
        print("2. List all the objects in a bucket ") 
        print("3. Upload an object ") 
        print("4. Download an object ") 
        print("5. Delete an object ") 
        print("6. Go to the main menu") 
        print("7. Exit program") 
        print("==================================================================")    
        option = input("Please insert the number of your option : ")
        print()
        if (option == "1"):
            # 1. List all the buckets
            s3.list_buckets()
        elif (option == "2"):
            # 2. List all the objects in a bucket
            s3.list_objects()
        elif (option == "3"):
            # 3. Upload an object
            s3.upload_object()
        elif (option == "4"):
            # 4. Download an object
            s3.download_object()
        elif (option == "5"):
            # 5. Delete an object
            s3.delete_object()
        elif (option == "6"):
            del s3
            return 0
        elif (option == "7"):
            del s3
            return 1
        else:
            error.not_valid_value(option)
        print()

def cw_menu (keys):
    # 
    # CW Menu:
    # This function shows the CW menu and request the user option.
    # It will create an instance of the CW class and invoke the
    # CW function/procedure requested by the user.
    # 
    cw = CW.CW(keys[1],keys[2])
    while True:
        print("==================================================================")
        print("CW Menu : ")
        print("1. Display 2 performance metrics ")
        print("2. Set an alarm ") 
        print("3. Go to the main menu") 
        print("4. Exit program") 
        print("==================================================================")    
        option = input("Please insert the number of your option : ")
        print()
        if (option == "1"):
            # 1. Display 2 performance metrics
            cw.show_metrics()
        elif (option == "2"):
            # 2. Set an alarm 
            cw.set_alarm()
        elif (option == "3"):
            del cw
            return 0
        elif (option == "4"):
            del cw
            return 1
        else:
            error.not_valid_value(option)
        print()
            

def menu (credentials):
    # 
    # Router menu:
    # This procedure is in charge of route the user to the differen submenus
    # depending on the chosen options.
    # 
    option = None
    is_exit = 0
    while ((option != 5) and (is_exit == 0)):
        service = main_menu()
        # EC2
        if (service == "1"):
            is_exit = ec2_menu(credentials)
        # EBS
        elif (service == "2"):
            is_exit = ebs_menu(credentials)
        # S3
        elif (service == "3"):
            is_exit = s3_menu(credentials)
        # CW
        elif (service == "4"):
            is_exit = cw_menu(credentials)
        # Exit program 
        elif (service == "5"):
            option = 5
        else:
            error.not_valid_value(service)






