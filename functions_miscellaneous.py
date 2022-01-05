import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

# Global variables
LARGE_FONT   =  ("Verdana", 12, 'bold')
BUTTON_FONT  = ("Arial", 10, 'bold')

# Function to show a page's help text
def help(help_section):

    helpBox = tk.Toplevel()

    if help_section == "MainMenu":
        help_title="Main Menu"
        text_to_print ="""
        Welcome to the GANSO main menu manual.

        This page allows three options:

            1. Network: Check information on the network components.
            
            2. Controller: Check information on the running ONOS controller.
            
            3. Network: Create, upload or check network slices."""

    elif help_section == "NetworkInfo":
        help_title="Network Information"
        text_to_print = """
        Welcome to the GANSO Network option manual.

        This option shows information on the network's underlying components:

            1. Switches: Show information on the network's forwarding devices (e.g. id, type, hardware, etc.).
            
            2. Hosts: Show information on the network's hosts (e.g. id, mac, IP address, etc.).
            
            3. Links: Show information on the links that connect the network's switches (e.g. port, type, device, etc.).
            
            4. Topology: Show information on the network's topology (e.g. uptime, devices, links, etc.).

            5. Cluster: Show information on the network's clusters (e.g. id, IP address, status, etc.).

            6. Configuration: Show information on the network's configuration."""

    elif help_section == "Login":
        help_title="Login"
        text_to_print = """
        Welcome to the GANSO Login page manual.

        This page allows logging in or creating a new user."""

    elif help_section == "NewUser":
        help_title="New User"
        text_to_print = """
        Welcome to the New GANSO user menu manual.

        This options allows creating a new user.

            1. GANSO information: Input the chosen GANSO username (must be unique) and password.

            2. ONOS information: Input the IP address and port where the ONOS controller is running as well as the ONOS username and password.

            All fields are mandatory."""

    elif help_section == "Controller":
        help_title="Controller"
        text_to_print = """

        Welcome to the GANSO Controller option manual.

        This option shows information on the ONOS controller:

            1. Flows: Show information on the OpenFlow flow entries currently installed in the network's forwarding devices (e.g. id, tableId, appId, etc.).

            2. Intents: Show the intents currently installed in the network's forwarding devices.

            3. Apps: Show information on the ONOS applications currently installed in the controller (e.g. name, id, version, etc.)."""

    elif help_section == "NetworkSlice":
        help_title="Network Slice"
        text_to_print = """
        Welcome to the GANSO Network slice option manual.

        This option allows creating, uploading or checking network slices.

            1. New slice: Create a new network slice by filling a GST form with the desired network slice properties.
            
            The Network slice name field must be filled and the name must be unique.
            
            The NEST file associated to the new network slice can be exported in XML format (check the "Export GST" option).
            
            To create the network slice the "Create Network Slice" option must be checked.
            
            2. Upload NEST: Choose an XML NEST file and create a network slice from it.
            
            3. View slices: Shows the XML NEST files of the created network slices."""

    # Scrollbars
    scrollbarVer = ttk.Scrollbar(helpBox)
    scrollbarVer.pack(side = "right", fill = "y")
    scrollbarHor = ttk.Scrollbar(helpBox, orient=tk.HORIZONTAL)
    scrollbarHor.pack(side = "bottom", fill = "x")

    tk.Label(helpBox, text=help_title + " page help", font = LARGE_FONT, height=2).pack()
    info = tk.Text(helpBox,yscrollcommand=scrollbarVer.set, xscrollcommand=scrollbarHor.set,wrap="none")
    info.pack(expand="yes",fill=tk.BOTH)

    scrollbarVer.config(command=info.yview)
    scrollbarHor.config(command=info.xview)

    info.insert(1.0, text_to_print)

# ================================================================================================================================== #

def outputFolder(title='Select output folder'):
            
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    folder_path = filedialog.askdirectory()
    return folder_path