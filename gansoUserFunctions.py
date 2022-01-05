import gansoMiscFunctions

import json
import re
import requests
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree import ElementTree

import xml.etree.ElementTree as ET
from pathlib import Path

# Global variables
LARGE_FONT   = ("Verdana", 12, 'bold')
BUTTON_FONT  = ("Arial", 10, 'bold')

# Validate user credentials
def userValidator(userName, userPwd):

    users_dir = Path("./users")

    # Open file containing users
    userFile = open(users_dir/"users.txt", 'r') 
    count = 0
    
    # Read users and passwords
    while True:

        count += 1
    
        # Get next line from file 
        currentLine = userFile.readline() 
    
        # End of file is reached 
        if not currentLine:
            userFile.close()
            return False

        userInfo = currentLine.rstrip().split(",")
        
        # Validate user and password
        if userInfo[0] == userName and userInfo[1] == userPwd:
            userFile.close()
            return True

# ================================================================================================================================== #

# Checks if user exists
def userExists(userName):

    users_dir = Path("./users")

    # Open file containing users
    userFile = open(users_dir/"users.txt", 'r')
    count = 0

    # Read users
    while True:

        count += 1

        # Get next line from file 
        currentLine = userFile.readline() 

        # End of file is reached 
        if not currentLine:
            userFile.close()
            return False

        # Validate user
        if currentLine.rstrip() == userName:
            userFile.close()
            return True

# ================================================================================================================================== #

# Create new GANSO user and User Information XML file
def createUserInfo(gansoUser, gansoPwd, ip1, ip2, ip3, ip4, port, onosUser, onosPwd):

    # Error code: Mandatory fields are empty
    if gansoUser == "" or gansoPwd == "" or ip1 == "" or ip2 == "" or ip3 == "" or ip4 == "" or port == "" or onosUser == "" or onosPwd == "":
        return 1

    # Error code: user already exists
    elif userExists(gansoUser):
        return 2

    # Error code: Invalid IP format
    elif not ip1.isdigit() or not ip2.isdigit() or not ip3.isdigit() or not ip4.isdigit() or not port.isdigit() or int(ip1) < 0 or int(ip1) > 255 \
         or int(ip2) < 0 or int(ip2) > 255 or int(ip3) < 0 or int(ip3) > 255 or int(ip4) < 0 or int(ip4) > 255 or int(port) < 0 or int(port) > 65535:
        return 3

    # Form correctly filled
    else:

        # Try connecting to ONOS
        try:
            onosUrl = "http://"+ip1+"."+ip2+"."+ip3+"."+ip4+":"+port+"/onos/v1/"
            request = requests.get(onosUrl + "devices", auth=(onosUser, onosPwd))

            # Successful connection
            if "\"devices\":" in request.text:

                users_dir = Path("./users")
                user_path = Path("./users/user_"+gansoUser)    

                # If switches does not exist, include User in Users file
                usersFile = open(users_dir/"users.txt", "a+")
                usersFile.write(gansoUser+"\n")

                # Create User Information XML file
                try:
                    os.mkdir(user_path)
                    
                    pathUserInfo = Path(user_path/"userInfo.xml")

                    root=Element('GANSO_user_information')
                    tree=ET.ElementTree(root)

                    # GANSO User Name
                    gansoUserXml = Element('GANSO_username')
                    root.append(gansoUserXml)
                    gansoUserXml.text = str(gansoUser)

                    # GANSO Password
                    gansoPwdXml = Element('GANSO_password')
                    root.append(gansoPwdXml)
                    gansoPwdXml.text = str(gansoPwd)

                    # ONOS IP
                    onosIpXml = Element('ONOS_URL')
                    root.append(onosIpXml)
                    onosIpXml.text = str(onosUrl)

                    # ONOS username
                    onosUserXml = Element('ONOS_username')
                    root.append(onosUserXml)
                    onosUserXml.text = str(onosUser)

                    # ONOS password
                    onosPwdXml = Element('ONOS_password')
                    root.append(onosPwdXml)
                    onosPwdXml.text = str(onosPwd)

                    # Write in User Information XML file
                    with open(pathUserInfo, 'wb') as f:
                        f.write(b'<?xml version="1.0" encoding="UTF-8"?>')
                        tree.write(f, xml_declaration=False, encoding='utf-8')
                    return 0

                # Error code: Unable to create user information file
                except OSError:
                    return 6

            # Error code: Connection to ONOS failed   
            else:
                return 5

        # Error code: Connection to ONOS failed
        except requests.exceptions.RequestException:
            return 5

# ================================================================================================================================== #

# Retrieves user information from User Information file
def getUserInfo(username):

    userInfo_path = Path("./users/user_"+username+"/userInfo.xml")

    root = ET.parse(userInfo_path).getroot()

    userInfo = [ 
        root.find('GANSO_username').text,
        root.find('GANSO_password').text,
        root.find('ONOS_URL').text,
        root.find('ONOS_username').text,
        root.find('ONOS_password').text
    ]
    
    return userInfo

# ================================================================================================================================== #

# Show error code in New User Creation form
def errorNewUser(newUser):
    
    # Error code: Mandatory field not filled
    if newUser == 1:
        label = "  Error: Please fill all fields             "
    # Error code: User already exists
    elif newUser == 2:
        label = "  Error: User already exists                "
    # Error code: Invalid IP or port format
    elif newUser == 3:
        label = "  Error: Invalid IP or port                 "
    # Error code: Invalid Swtich Id format
    elif newUser == 4:
        label = "  Error: Invalid Switch Id                  "                               
    # Error code: Unable to connect with ONOS
    elif newUser == 5:
        label = "  Error: Connection with ONOS failed        "
    # Error code: Unable to create User Information file
    elif newUser == 6:
        label = "  Error: File not created                   "
    # Error code: Successful operation
    else:
        label = "  Success!                                  "

    return label

# ================================================================================================================================== #