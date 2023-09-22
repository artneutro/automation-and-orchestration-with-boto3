#!/usr/bin/env python3
# 
# Author: Jose Lo Huang
# Creation Date: 20/11/2020
# Updates:
# 21/11/2020 - Add the getpass package to hide the password in Python.
# 01/12/2020 - Minor fixes and add comments for better read.
# 
# This program will be in charge of the following 3 main tasks:
# 1. Request and check credentials (login/password)
# 2. Print the main management menu
# 3. Execute the requested AWS task
# 


import getpass
import Menus


def request_login ():
    # 
    # This function will request for the login username and password
    # and check if they exists on the 'passwd.txt' file.
    # It returns:
    # 0  = incorrect username or password
    # 1  = correct username and password
    # -1 = user hit 'Enter' as username to exit
    # 
    username = input("Please enter your username : ")
    # User wants to exit program
    if (username == None) or (username == ""):
        return [-1]
    try:
        password = getpass.getpass("Please enter your password : ")
    except:
        pass
    try:
        with open('passwd.txt') as passwd:
            lines = passwd.readlines()
            for line in lines:
                if (username == line.strip().split()[0]):
                    if (password == line.strip().split()[1]):
                        # If username and password are correct, then returns
                        # a list including the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
                        return [1, line.strip().split()[2] , line.strip().split()[3]]
                    else:
                        # Incorrect password
                        return [0]
            # Incorrect username
            return [0]
    except:
        print("The password file is incorrect, was removed or the permissions are invalid.")


def main():
    # 
    # MAIN PROGRAM
    #
    print("==================================================================")
    print("AWS Manager v1.0 powered by CIT, AWS, Python3 and Boto3           ")
    print("Author: Jose Lo Huang. All rights reserved using the MIT License. ")
    print("Complete instructions on the README.txt file. Hit 'ENTER' to exit.")
    print("==================================================================")
    while True:
        #correct_credentials = [1,'AKIA****************','*****************************']
        correct_credentials = request_login()
        # Correct username and password
        if correct_credentials[0] == 1 :
            Menus.menu(correct_credentials)
            print("Program finished.")
            break
        # Incorrect username or password
        elif correct_credentials[0] == 0 :
            print("Incorrect credentials. Try again.")
        # User hit 'Enter' as username to exit
        elif correct_credentials[0] == -1 :
            print("Program finished.")
            break


#
# PROGRAM RUN
# 
main()



