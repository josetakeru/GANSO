﻿# GANSO
## GST And Network Slice Operator

GANSO is a software built as part of a research effort focused on 5G and network slicing which culminated in the publication of the paper [GANSO: Automate Network Slicing at the Transport Network Interconnecting the Edge](https://ieeexplore.ieee.org/document/9289875).

GANSO allows users to fill in *Generic network Slice Templates* (*GST*) to create *network slices* over an existing SDN. These slices can be tuned to cater to a user or company's specific needs by setting rules - e.g to set a rate limit or user data access - without having to build their own networks.

<br />

## Requirements

### GANSO environment

GANSO leverages on the *[mininet](http://mininet.org/download/)* and *[ONOS](https://opennetworking.org/onos/)* tools to create virtual networks and their SDN controllers respectively. To install, configure and run these, you can refer to the *[GANSO_environment_installer](https://github.com/josetakeru/GANSO_environment_installer)* or do it manually.

### GANSO

To run GANSO, *python3* must be installed in the GANSO running machine. Additionally, the *tkinter*, *jq*, *requests*, *pathlib* and *xml* modules are required

<br />

## Running GANSO

To run GANSO, use *python* command (or *python3* if it is not redirecting to such version by default):

    python main.py

This will start the GANSO GUI which can be used to create different virtual rules in the created network.

<img src="resources/man/ganso_start_page.png">


### User login page


#### Creating a GANSO user

To create a new GANSO user click on the *New user* option within the *Login page*.

<img src="resources/man/ganso_login_new_user_button.png">


This will take you to the *New GANSO user* page where you can fill in the details of your setup:
* **GANSO information:**
    * *User*: User name used to login into and use GANSO (*note: must be unique*).
    * *Pass*: Password used to login into and use GANSO (*note: this is stored as a plain string as it is only in a proof of concept stage*).

* **ONOS information:**
    * *IP*: IP of the host where the environment is running (127.0.0.1 if it is the same as that of GANSO).
    * *Port*: Port in which ONOS controller is exposed (default: 8181).
    * *User*: User name used to login into ONOS (default: *onos*).
    * *Pass*: Password used to login into ONOS (default: *rocks*).


After inputting the new GANSO user's information click Next and wait for the program to check if it can connect to ONOS.

<img src="resources/man/ganso_login_new_user_page.png">

#### Logging in on with an existing GANSO user

If you already have a GANSO user, you can use it to log into GANSO provided that it has been setup correctly and that the environment (i.e. *mininet* and *ONOS*) is running.


### GANSO main menu

GANSO's main menu allows three options: *Network*, *Controller* and *Network slice*.

<img src="resources/man/ganso_main_menu_page.png">


### GANSO Network option

The *Network information* menu allows showing information on the network's components i.e. the switches, hosts, etc.

<img src="resources/man/ganso_network_option.png">
 

### GANSO Controller option

The *Controller information* menu allows showing information on the ONOS controller i.e. the flows, intents, etc.

<img src="resources/man/ganso_controller_option.png">


### GANSO Network slice option

The *Network slice* menu allows creating, uploading and showing network slices. 

<img src="resources/man/ganso_network_slice_option.png">
 

#### New slice option

To create a new network slice fill in the *network slice form* with the rules you want to enforce and the hosts that should be affected by them. Additionally, you can export the template in an XML format. 

<img src="resources/man/ganso_network_slice_form.png">


#### Upload NEST option

To create a network slice from a template, you can upload a *NEST* (*NEtwork Slice Type*) file which needs to be in an XML format.


#### View slices option

This option shows the network slices that have been created in the network.
