# GANSO
## GST And Network Slice Operator

GANSO is a software built as part of a research effort focused on 5G and network slicing which culminated in the publication of the paper [GANSO: Automate Network Slicing at the Transport Network Interconnecting the Edge](https://ieeexplore.ieee.org/document/9289875).

GANSO allows users to fill in *Generic network Slice Templates* (*GST*) and create network slices tuned to their specific needs (e.g. setting their own rate limit or user data access) without having to build their own networks.

## Requirements

### GANSO

To run GANSO, python3 must be installed in the machine. Additionally, the *tkinter*, *jq*, *requests*, *pathlib* and *xml* modules are required

### Environment: mininet and ONOS

This software leverages on the [mininet](http://mininet.org/download/) and [ONOS](https://opennetworking.org/onos/) tools to create virtual networks and their SDN controllers respectively. These may be run on a different host or VM than that on which GANSO will be executed as long as all machines are able to talk to each other. You can use the *resources/setup_environment.sh* script to install, configure and run the environment on a Debian machine (*note: you will need sudo priviledges to run it since it installs the necessary packages*).

## Running GANSO

To run GANSO, first start ONOS and mininet on the environment host either manually or through the provided script:

Manually:

    > sudo /opt/onos/bin/onos-service start
    > sudo systemctl start openvswitch-switch
    > sudo mn --custom "${mn_custom_topo_file}" --controller remote,ip=127.0.0.1 --switch=ovs,protocols=OpenFlow13 --nat --topo "${mn_custom_topo_name}"

Through script:

    > sudo ./resources/setup_environment.sh

Once the environment is up, run the software on the GANSO host:

    > python main.py

This will start the GANSO GUI which can be used to create different virtual rules in the created network.