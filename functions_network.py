import functions_show_help

import json
import re
import requests
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from shutil import copyfile

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree import ElementTree
import xml.dom.minidom

import xml.etree.ElementTree as ET
from pathlib import Path

# Global variables
LARGE_FONT   = ("Verdana", 12, 'bold')
BUTTON_FONT  = ("Arial", 10, 'bold')

# ================================================================================================================================== #

# Returns network information
def getSwitches(onosUrl, onosUsr, onosPwd):

    onosUrl = onosUrl + "devices"
    request = json.loads(requests.get(onosUrl, auth=(onosUsr, onosPwd)).text)
    switches = []

    for i in range(len(request["devices"])):
        switches.append(json.dumps(request["devices"][i]["id"]))
        switches[i] = switches[i].replace('\"', '')

    return switches

# ================================================================================================================================== #

# Show information of an element    
def showNetInfo(showOption, switches, onosUrl, onosUsr, onosPwd):

    infoBox = tk.Toplevel()

    # Scrollbars
    scrollbarVer = ttk.Scrollbar(infoBox)
    scrollbarVer.pack(side = "right", fill = "y")
    scrollbarHor = ttk.Scrollbar(infoBox, orient=tk.HORIZONTAL)

    # Page description
    tk.Label(infoBox, text="Network " + showOption + ": ", font = LARGE_FONT, height=2).pack()
    info = tk.Text(infoBox,yscrollcommand=scrollbarVer.set, xscrollcommand=scrollbarHor.set,wrap="none")
    info.pack(expand="yes",fill=tk.BOTH)

    scrollbarHor.pack(side = "bottom", fill = "x")
    scrollbarVer.config(command=info.yview)
    scrollbarHor.config(command=info.xview)

    onosUrl += showOption
    request = requests.get(onosUrl, auth=(onosUsr, onosPwd))
    aux = json.loads(request.text)
    info.insert(tk.END, json.dumps(aux, indent=2))

# ================================================================================================================================== #

# Show information of an element    
def showControllerInfo(showOption, optionId, switches, onosUrl, onosUsr, onosPwd):

    infoBox = tk.Toplevel()

    # Scrollbars
    scrollbarVer = ttk.Scrollbar(infoBox)
    scrollbarVer.pack(side = "right", fill = "y")
    scrollbarHor = ttk.Scrollbar(infoBox, orient=tk.HORIZONTAL)

    # Page description
    tk.Label(infoBox, text="Controller " + showOption + ": "+ optionId, font = LARGE_FONT, height=2).pack()
    info = tk.Text(infoBox,yscrollcommand=scrollbarVer.set, xscrollcommand=scrollbarHor.set,wrap="none")
    info.pack(expand="yes",fill=tk.BOTH)

    scrollbarHor.pack(side = "bottom", fill = "x")
    scrollbarVer.config(command=info.yview)
    scrollbarHor.config(command=info.xview)

    onosUrl += showOption

    if showOption == "flows" and optionId != "":
        for x in range(len(switches)):
            
            onosUrlAux = onosUrl + "/"+ switches[x] + "/"+optionId
            request = requests.get(onosUrlAux, auth=(onosUsr, onosPwd))

            if "404" not in request.text:

                aux = json.loads(request.text)
                info.insert(tk.END, json.dumps(aux, indent=2))

    else:

        if optionId != "":
            onosUrl += "/" + optionId
            
        request = requests.get(onosUrl, auth=(onosUsr, onosPwd))
        aux = json.loads(request.text)
        info.insert(tk.END, json.dumps(aux, indent=2))

# ================================================================================================================================== #

# Show GST form
def newGst(username, switches, onosUrl, onosUsr, onosPwd):

    gstForm = tk.Toplevel()
    gstForm.geometry("400x450")
    tk.Tk.resizable(gstForm,width=False, height=False)

    pageTitle = tk.Label(gstForm, text="      New network slice", font = LARGE_FONT, height=2)
    pageTitle.grid(row=0, column=1, columnspan = 6)
    
    # Slice Name
    tk.Label(gstForm, text="        Network slice name: ").grid(row=1, column=2,sticky="w")
    entrySliceName = ttk.Entry(gstForm, width=20)
    entrySliceName.grid(row=1, column=3, sticky="w", columnspan=5)

    # Slice Industry
    industryList = [
        "None",
        "None",
        "Virtual Reality",
        "Automotive",
        "Energy",
        "Healthcare",
        "Industry 4.0",
        "IoT",
        "Public safety",
    ]
    
    tk.Label(gstForm, text="        Slice industry: ").grid(row=2, column=2,sticky="w")
    clickIndustry = tk.StringVar()
    clickIndustry.set(industryList[0])
    dropIndustryList = ttk.OptionMenu(gstForm, clickIndustry, *industryList)
    dropIndustryList.grid(row=2,column=3,sticky="w", columnspan=4)

    # Rate limit slice
    tk.Label(gstForm, text="        Rate limit (empty if none): ").grid(row=4, column=2,sticky="w")
    rateLimitSlice = ttk.Entry(gstForm, width=12)
    rateLimitSlice.grid(row=4, column=3, sticky="w")
    tk.Label(gstForm, text="kbps").grid(row=4, column=4,sticky="w")

    # Rate limit hosts
    tk.Label(gstForm, text="        Hosts (IPs split by commas): ").grid(row=5, column=2,sticky="w")
    rateLimitHosts = ttk.Entry(gstForm, width=25)
    rateLimitHosts.grid(row=5, column=3,columnspan=15)

    # Slice User data access
    userDataList = [
        "0 - Internet (default)",
        "0 - Internet (default)",
        "1 - Private network",
        "2 - No traffic",
    ]
    
    tk.Label(gstForm, text="        User data access: ").grid(row=7, column=2,sticky="w")
    userDataslice = tk.StringVar()
    userDataslice.set(userDataList[0])
    dropList = ttk.OptionMenu(gstForm, userDataslice, *userDataList)
    dropList.grid(row=7,column=3,sticky="w",columnspan=3)

    # Input host IPs
    tk.Label(gstForm, text="        Hosts (IPs split by commas): ").grid(row=8, column=2,sticky="w")
    userDataHosts = ttk.Entry(gstForm, width=25)
    userDataHosts.grid(row=8, column=3,columnspan=15)

    # Export GST
    exportGST = tk.IntVar()
    exportCheck = tk.Checkbutton(gstForm, text = "Export GST", variable=exportGST)
    exportCheck.grid(row = 10, column=3, columnspan=4,sticky="w")
    
    # Create Network slice
    createNetSlice = tk.IntVar()
    netSliceCheck = tk.Checkbutton(gstForm, text = "Create Network Slice", variable=createNetSlice)
    netSliceCheck.grid(row = 11, column=3, columnspan=4,sticky="w")
   
    # Action buttons
    buttonExit = ttk.Button(gstForm, text="Cancel", command=gstForm.destroy)
    buttonExit.grid(row=14,column=3,sticky="e")
    buttonCreate = ttk.Button(gstForm, text="Create", command=lambda: confirmGst(username, entrySliceName.get(), clickIndustry.get(), rateLimitSlice.get(), \
        rateLimitHosts.get(), userDataslice.get(), userDataHosts.get(), exportGST.get(), createNetSlice.get(), switches, onosUrl, onosUsr, onosPwd))
    buttonCreate.grid(row=14,column=4,sticky="e")
   
    def confirmGst(username, sliceName, industry, rateLimit, rateLimitHosts, userDataAccess, userDataHosts, exportGST, createNetSlice, switches, onosUrl, onosUsr, onosPwd):
        
        warningLabel = tk.Label(gstForm, text="")

        errorLabel = createGst(username, sliceName, industry, rateLimit, rateLimitHosts, userDataAccess, userDataHosts, exportGST, createNetSlice, switches, onosUrl, onosUsr, onosPwd)
        warningLabel = tk.Label(gstForm, text=errorLabel)
        warningLabel.grid(row=13,column=1,columnspan=7,sticky='w')
        
        if errorLabel == "Success!                                             ":
            gstForm.destroy()

    # GUI formatting
    gstForm.grid_rowconfigure(0, minsize=60)
    gstForm.grid_rowconfigure(1, minsize=30)
    gstForm.grid_rowconfigure(2, minsize=30)
    gstForm.grid_rowconfigure(3, minsize=30)
    gstForm.grid_rowconfigure(4, minsize=30)
    gstForm.grid_rowconfigure(5, minsize=30)
    gstForm.grid_rowconfigure(6, minsize=30)
    gstForm.grid_rowconfigure(7, minsize=30)
    gstForm.grid_rowconfigure(8, minsize=30)
    gstForm.grid_rowconfigure(9, minsize=30)
    gstForm.grid_rowconfigure(10, minsize=20)
    gstForm.grid_rowconfigure(11, minsize=20)
    gstForm.grid_rowconfigure(12, minsize=20)
    gstForm.grid_rowconfigure(13, minsize=20)
    gstForm.grid_rowconfigure(14, minsize=20)

# ================================================================================================================================== #

def createGst(username, sliceName, industry, rateLimit, rateLimitHosts, userDataAccess, userDataHosts, exportGST, createNetSlice, switches, onosUrl, onosUsr, onosPwd):

    netSlices_dir = Path("./resources/network_slices")

    rateLimitHosts = rateLimitHosts.replace(" ", "").split(',')
    userDataHosts = userDataHosts.replace(" ", "").split(',')

    root=Element('GST')
    tree=ET.ElementTree(root)

    if sliceName == "": 
        return "        Error: Please fill all obligatory fields             "
    elif industry == "Select":
        return "        Error: Please choose an industry                     "
    elif rateLimit == "":
        rateLimit = 0
    elif not rateLimit.isdigit() or int(rateLimit) <= 0:
        return "        Error: Rate limit must be a positive integer         "
    elif userDataAccess == "Select":
        return "        Error: Please choose User data access option         "
    elif netSliceExists(username, sliceName):
        return "        Error: Network slice name already exists             "

    # Slice Name
    sliceNameXml=Element('slice_name')
    root.append(sliceNameXml)
    sliceNameXml.text = str(sliceName)

    # Slice Industry
    industryXml=Element('industry')
    root.append(industryXml)
    industryXml.text = str(industry)

    # Rate limit slice
    rateLimitXml=Element('rate_limit')
    root.append(rateLimitXml)
    rateLimitValueXml = ET.SubElement(rateLimitXml, 'value')
    rateLimitValueXml.text = "None" if rateLimit == "" else str(rateLimit)
    rateLimitHostsXml = ET.SubElement(rateLimitXml, 'hosts')

    for i in range(len(rateLimitHosts)):
        hostIp = ET.SubElement(rateLimitHostsXml,'host_ip')
        hostIp.text = str(rateLimitHosts[i])

    # Slice User data access
    userDataAccessXml = Element('user_data_access')
    root.append(userDataAccessXml)
    userDataAccessValueXml = ET.SubElement(userDataAccessXml, 'value')
    userDataAccessValueXml.text = str(userDataAccess)
    userDataHostsXml = ET.SubElement(userDataAccessXml, 'hosts')

    for i in range(len(userDataHosts)):
        hostIp = ET.SubElement(userDataHostsXml,'host_ip')
        hostIp.text = str(userDataHosts[i])

    slice_file = sliceName + ".xml"

    with open(netSlices_dir/slice_file, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>')
        tree.write(f, xml_declaration=False, encoding='utf-8')

    if exportGST == 1:
        
        outputPath = functions_show_help.outputFolder()

        if outputPath != '':

            slice_file = "GANSO_slice_"+ sliceName + ".xml"
            output_file = Path(outputPath)

            with open(output_file/slice_file, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="UTF-8"?>')
                tree.write(f, xml_declaration=False, encoding='utf-8')
            
    if createNetSlice == 1:

        createNetworkSlice(sliceName, switches, onosUrl, onosUsr, onosPwd, False)



    # If switches does not exist, include network slice in netSlices file
    netSlicesFile = open(netSlices_dir/"netSlices.txt", "a+")
    netSlicesFile.write(sliceName+"\n")
    netSlicesFile.close()

    return "Success!                                             "

# ================================================================================================================================== #

def showSlices():

    helpBox = tk.Toplevel()

    # Scrollbars
    scrollbarVer = ttk.Scrollbar(helpBox)
    scrollbarVer.pack(side = "right", fill = "y")
    scrollbarHor = ttk.Scrollbar(helpBox, orient=tk.HORIZONTAL)
    scrollbarHor.pack(side = "bottom", fill = "x")

    tk.Label(helpBox, text="Created network slices", font = LARGE_FONT, height=2).pack()
    info = tk.Text(helpBox,yscrollcommand=scrollbarVer.set, xscrollcommand=scrollbarHor.set,wrap="none")
    info.pack(expand="yes",fill=tk.BOTH)

    scrollbarVer.config(command=info.yview)
    scrollbarHor.config(command=info.xview)

    netSlices_dir = Path("./resources/network_slices")

    # Open file containing users
    netSlicesFile = open(netSlices_dir/"netSlices.txt", 'r') 
    count = 0

    # Read users
    while True:

        count += 1

        # Get next line from file 
        netSliceName = netSlicesFile.readline().replace('\n', '')

        # End of file is reached 
        if not netSliceName:
            netSlicesFile.close()
            return False
        
        netSliceXML = netSliceName + '.xml'
        file = open(netSlices_dir/netSliceXML, 'r')

        dom = xml.dom.minidom.parse(file)

        info.insert(1.0, dom.toprettyxml())
        info.insert(1.0, '\n')
        info.insert(1.0, '==========================================================================\n')
        info.insert(1.0, '\n')

    return True

# ================================================================================================================================== #

def createNetworkSlice(sliceName, switches, onosUrl, onosUsr, onosPwd, uploaded):

    if uploaded:
        netSlices_dir = Path("./resources/network_slices")
        gstPath = sliceName
        sliceName = sliceName.split("/")
        sliceName = sliceName[len(sliceName)-1]
        netSlicesFile = open(netSlices_dir/"netSlices.txt", "a+")
        netSlicesFile.write(sliceName.replace('.xml',"")+"\n")
        netSlicesFile.close()
        copyfile(gstPath, netSlices_dir/sliceName)      
    else:
        gstPath = Path("./resources/network_slices/" + sliceName + ".xml")    
    rateLimitHosts = []
    userDataHosts = []
    root = ET.parse(gstPath).getroot()

    for i in root.findall('rate_limit/value'):
        rateLimit = i.text

    if int(rateLimit) > 0:

        for i in root.findall('rate_limit/hosts/host_ip'):
            rateLimitHosts.append(i.text)

        for i in range(len(switches)):
            rateLimitRule(rateLimit, 50000, switches[i], rateLimitHosts, onosUrl, onosUsr, onosPwd)

    for i in root.findall('user_data_access/value'):
        userDataAccess = i.text

    for i in root.findall('user_data_access/hosts/host_ip'):
        userDataHosts.append(i.text)

    for i in range(len(switches)):
        userDataAccessRule(userDataAccess, 50000, switches[i], userDataHosts, onosUrl, onosUsr, onosPwd)

# ================================================================================================================================== #

# Function to create rate limit rule
def rateLimitRule(rateLimit, priority, switchId, hosts, onosUrl, onosUsr, onosPwd):

    flow_rules_dir = Path("./resources/flow_rules")

    # FALTA: ASIGNAR A LOS VLAN ID
    for j in range(len(hosts)):    
        meterId = 0
        
        urlMeter = onosUrl+"meters/" + switchId
        with open(flow_rules_dir/'rateLimitMeters.json') as json_file:
            meterJson = json.load(json_file)

        meterJson["deviceId"] = switchId
        meterJson["bands"][0]["rate"] = int(rateLimit)

        requests.post(urlMeter, auth=(onosUsr, onosPwd), json = meterJson)
        meterReq = requests.get(urlMeter, auth=(onosUsr, onosPwd)).json()

        for i in range(len(meterReq["meters"])):

            aux = meterReq["meters"][i]["id"]        
            aux = int(aux, 16)

            if aux > meterId:
                meterId = aux

        urlFlow = onosUrl+"flows/"+switchId+"?appId=*.core"

        flow_rules_dir = Path("./resources/flow_rules")

        with open(flow_rules_dir/'rateLimitFlows.json') as json_file:
            flowJson = json.load(json_file)

        flowJson["priority"] = priority

        flowJson["treatment"]["instructions"][0]["meterId"] = str(meterId)
        flowJson["deviceId"] = switchId

        flowJson["selector"]["criteria"][1]["ip"] = hosts[j]+"/32"

        for x in range(2):
            flowJson["tableId"] = x            
            requests.post(urlFlow, auth=(onosUsr, onosPwd), json = flowJson)
        
# ================================================================================================================================== #

# Function to user data access rule
def userDataAccessRule(userDataAccess, priority, switchId, hosts, onosUrl, onosUsr, onosPwd):
    
    urlFlow = onosUrl+"flows/"+switchId+"?appId=*.core"
    flow_rules_dir = Path("./resources/flow_rules")

    if userDataAccess == "1 - Private network":
        
        with open(flow_rules_dir/'userDataFlows_PrivateNetwork.json') as json_file1:
            flowJson1 = json.load(json_file1)

        flowJson1["priority"] = 60000
        flowJson1["deviceId"] = switchId
        flowJson1["treatment"]["instructions"]= [{"type":"TABLE", "tableId": "1"}]
#        flowJson1["treatment"]["instructions"]= [{"type":"OUTPUT", "port": "CONTROLLER"}]
        flowJson1["selector"]["criteria"][1]["ip"] = "10.0.0.0/16"

        with open(flow_rules_dir/'userDataFlows_PrivateNetwork.json') as json_file2:
            flowJson2 = json.load(json_file2)

        flowJson2["priority"] = 55000
        flowJson2["deviceId"] = switchId
        flowJson2["selector"]["criteria"][1]["ip"] = "10.0.0.0/1"

        # FALTA: ASIGNAR A LOS VLAN ID
        for j in range(len(hosts)):
            flowJson1["selector"]["criteria"][2]["ip"] = hosts[j]+"/32"
            requests.post(urlFlow, auth=(onosUsr, onosPwd), json = flowJson1)

            flowJson2["selector"]["criteria"][2]["ip"] = hosts[j]+"/32"
            requests.post(urlFlow, auth=(onosUsr, onosPwd), json = flowJson2)

    elif userDataAccess == "2 - No traffic":
        
        with open(flow_rules_dir/'userDataFlows_NoConnection.json') as json_file:
            flowJson = json.load(json_file)

        flowJson["deviceId"] = switchId

        # FALTA: ASIGNAR A LOS VLAN ID
        for j in range(len(hosts)):
            
            flowJson["selector"]["criteria"][1]["ip"] = hosts[j]+"/32"
            requests.post(urlFlow, auth=(onosUsr, onosPwd), json = flowJson)

# ================================================================================================================================== #

# Checks if Network slice exists
def netSliceExists(userName, netSliceName):

    netSlices_dir = Path("./resources/network_slices")

    # Open file containing users
    netSlicesFile = open(netSlices_dir/"netSlices.txt", 'r') 
    count = 0

    # Read users
    while True:

        count += 1

        # Get next line from file 
        currentLine = netSlicesFile.readline() 

        # End of file is reached 
        if not currentLine:
            netSlicesFile.close()
            return False

        # Validate user
        if currentLine.rstrip() == netSliceName:
            netSlicesFile.close()
            return True
