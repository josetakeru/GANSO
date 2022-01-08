# GANSO
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

<br />