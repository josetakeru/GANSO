import gansoMiscFunctions
import gansoNetworkFunctions
import gansoUserFunctions
from io import BytesIO
import json
import re
import requests

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET


# Global variables
LARGE_FONT   =  ("Verdana", 12, 'bold')
BUTTON_FONT  = ("Arial", 10, 'bold')
GANSO_USR    = ""
ONOS_URL     = ""
ONOS_USR     = ""
ONOS_PWD     = ""
SWITCHES     = []

# Loads the frame and pages of the GUI
class GansoApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        # Load program GUI frame
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, default="Resources\\Images\\gansoIcon.ico")
        tk.Tk.wm_title(self, "GANSO - GST And Network Slice Operator")
        tk.Tk.resizable(self,width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True, padx=5, pady=5)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Load pages
        PAGES = [
            PageController,
            PageLogin,
            PageMainMenu,
            PageNetInfo,
            PageNetSlice,
            PageNewUser,            
            PageStart
        ]
        
        for page in PAGES:
        
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="snew")
        
        self.show_frame(PageStart)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

# ================================================================================================================================== #

# Welcome page - Shows user that GANSO app is now running
class PageStart(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        # Main picture
        self.photo = tk.PhotoImage(file=".\\Resources\\Images\\gansoLogo.png")
        pagePic = tk.Label(self, image=self.photo)
        pagePic.grid(row=0,column=0,columnspan = 2)
        
        # Action Buttons
        buttonNext = ttk.Button(self, text="Start", command=lambda: controller.show_frame(PageLogin))
        buttonNext.grid(row=2,column=0,sticky="s", columnspan=2)
        
        self.grid_rowconfigure(2, minsize=25)
        
# ================================================================================================================================== #

# Login page - Allows login and new user creation
class PageLogin(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        # Page description
        pageTitle = tk.Label(self, text = "Login page", font = LARGE_FONT)
        pageTitle.grid(row=0, column=3, columnspan=9, sticky="w")
        loginIcon = tk.PhotoImage(file="Resources\\Images\\loginIcon.png")
        self.newUserIcon = tk.PhotoImage(file="Resources\\Images\\newUserIcon.png")

        # Login - User and password
        tk.Label(self, text="Username: ", width = 8).grid(row=2, column=1,sticky="w")
        entryUser = ttk.Entry(self, width=12)
        entryUser.grid(row=2, column=2, sticky ="w")
        tk.Label(self, text="Password:   ", width = 8).grid(row=3, column=1,sticky="w")
        entryPwd = ttk.Entry(self, width=12, show="*")
        entryPwd.grid(row=3, column=2, sticky ="w")
        buttonLogin = ttk.Button(self, image=loginIcon,command=lambda: login(entryUser.get(), entryPwd.get()))
        buttonLogin.image = loginIcon
        buttonLogin.grid(row=4,column=2, sticky="e")
        
        # New user option
        tk.Label(self, image=self.newUserIcon).grid(row=2, column=6,rowspan=2)
        buttonNewUser = ttk.Button(self, text="New user", width=10, command=lambda: controller.show_frame(PageNewUser))
        buttonNewUser.grid(row=4, column=6,sticky="w")
        
        # Action buttons
        buttonHelp = ttk.Button(self, text="Help", command=lambda: gansoMiscFunctions.help("Login"))
        buttonHelp.grid(row=7,column=0,sticky="s")
 
        # GUI formatting
        tk.Label(self, text="or", width = 18).grid(row=3, column=4)
        tk.Label(self, text="", width=3).grid(row=2, column=0)
        self.grid_rowconfigure(0, minsize=50)
        self.grid_rowconfigure(1, minsize=30)
        self.grid_rowconfigure(2, minsize=30)
        self.grid_rowconfigure(3, minsize=30)
        self.grid_rowconfigure(4, minsize=10)
        self.grid_rowconfigure(5, minsize=10)
        self.grid_rowconfigure(6, minsize=25)

        # Go to main menu page if user and password are correct
        def login(user, password):

            if gansoUserFunctions.userExists(user):
                userInfo = gansoUserFunctions.getUserInfo(user)

                if password == userInfo[1]:

                    global GANSO_USR, ONOS_URL, ONOS_USR, ONOS_PWD, SWITCHES
                    GANSO_USR = userInfo[0]
                    ONOS_URL  = userInfo[2]
                    ONOS_USR  = userInfo[3]
                    ONOS_PWD  = userInfo[4]
                    SWITCHES   = gansoNetworkFunctions.getSwitches(ONOS_URL, ONOS_USR, ONOS_PWD)

                    controller.show_frame(PageMainMenu)

                    ethType = ["0x8942", "0x806", "0x88cc", "0x800"]

                    for i in range(len(SWITCHES)):

                        for x in range(len(ethType)):

                            with open('Resources\\flowNewTable.json') as json_file:
                                jsonFile = json.load(json_file)
                                jsonFile["deviceId"] = SWITCHES[i]
                                jsonFile["selector"]["criteria"][0]["ethType"] = ethType[x]
                                requests.post(ONOS_URL + "flows/" + SWITCHES[i], auth=(ONOS_USR, ONOS_PWD), json = jsonFile)

                else:
                    tk.Label(self, text="Warning: Invalid user or password").grid(row=7, column=3,columnspan=8, sticky="w")

            else:
                tk.Label(self, text="Warning: Invalid user or password").grid(row=7, column=3,columnspan=8, sticky="w")

# ================================================================================================================================== #

# New user page - Allows user creation through form
class PageNewUser(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        # Page description
        pageTitle = tk.Label(self, text = "New GANSO user", font = LARGE_FONT)
        pageTitle.grid(row=0, column=6, columnspan=15,sticky="w")
        pageInfo = tk.Label(self, text="GANSO information: ")
        pageInfo.grid(row=1, column=1, sticky="w", columnspan = 9)
        pageInfo = tk.Label(self, text="ONOS information: ")
        pageInfo.grid(row=1, column=6, sticky="w", columnspan = 20)
        
        # Input new GANSO user and password
        tk.Label(self, text="User: ", width = 8).grid(row=2, column=2,sticky="w")
        entryGansoUser = ttk.Entry(self, width=10)
        entryGansoUser.grid(row=2, column=3, sticky ="w")
        tk.Label(self, text="Pass: ", width = 8).grid(row=3, column=2,sticky="w")
        entryGansoPwd = ttk.Entry(self, width=10, show="*")
        entryGansoPwd.grid(row=3, column=3, sticky ="w")

        # Input ONOS IP
        tk.Label(self, text="IP: ").grid(row=2, column=7,sticky="w")
        entryIP1 = ttk.Entry(self, width=3)
        entryIP1.grid(row=2, column=8,sticky="w")
        tk.Label(self, text=".").grid(row=2, column=9,sticky="w")
        entryIP2 = ttk.Entry(self, width=3)
        entryIP2.grid(row=2, column=10,sticky="w")
        tk.Label(self, text=".").grid(row=2, column=11,sticky="w")
        entryIP3 = ttk.Entry(self, width=3)
        entryIP3.grid(row=2, column=12,sticky="w")
        tk.Label(self, text=".").grid(row=2, column=13,sticky="w")
        entryIP4 = ttk.Entry(self, width=3)
        entryIP4.grid(row=2, column=14,sticky="w")

        # Input ONOS port
        tk.Label(self, text="Port: ").grid(row=3,column=7,sticky="w")
        entryPort = ttk.Entry(self, width=10)
        entryPort.grid(row=3, column=8, sticky="w",columnspan=10)

        # Input ONOS user and password
        tk.Label(self, text="User: ").grid(row=2, column=16,sticky="w")
        entryOnosUser = ttk.Entry(self, width=10)
        entryOnosUser.grid(row=2, column=17,sticky="w",columnspan=5)
        tk.Label(self, text="Pass:  ").grid(row=3, column=16, sticky="w")
        entryOnosPwd = ttk.Entry(self, width=10, show="*")
        entryOnosPwd.grid(row=3, column=17,sticky="w",columnspan=5)

        # Action buttons
        buttonHelp = ttk.Button(self, text="Help", command=lambda: gansoMiscFunctions.help("NewUser"))
        buttonHelp.grid(row=8,column=0,sticky="se",columnspan=5)
        buttonBack = ttk.Button(self, text="<< Back", command=lambda: controller.show_frame(PageLogin))
        buttonBack.grid(row=8,column=14,sticky="w",columnspan=5)
        buttonNext = ttk.Button(self, text="Next >>", command=lambda: nextPage(entryGansoUser.get(), entryGansoPwd.get(), entryIP1.get(), \
            entryIP2.get(), entryIP3.get(), entryIP4.get(), entryPort.get(), entryOnosUser.get(), entryOnosPwd.get()))
        buttonNext.grid(row=8,column=17,sticky="es",columnspan=5)
        
        # GUI formatting
        tk.Label(self, text="", width = 5).grid(row=1, column=5)
        tk.Label(self, text="", width = 1).grid(row=2, column=0)
        tk.Label(self, text="", width = 1).grid(row=2, column=1)
        tk.Label(self, text="", width = 1).grid(row=2, column=6)
        tk.Label(self, text="", width = 1).grid(row=2, column=15)
        self.grid_rowconfigure(0, minsize=50)
        self.grid_rowconfigure(1, minsize=30)
        self.grid_rowconfigure(2, minsize=30)
        self.grid_rowconfigure(3, minsize=30)
        self.grid_rowconfigure(4, minsize=25)
        self.grid_rowconfigure(5, minsize=25)
        self.grid_rowconfigure(6, minsize=25)

        # Go to main menu page if input information is correct
        def nextPage(gansoUser, gansoPwd, ip1, ip2, ip3, ip4, port, onosUser, onosPwd):

            textLabel = tk.Label(self, text="  Trying to connect with ONOS, please wait")
            textLabel.grid(row=6, column=3,columnspan=15, sticky="w")

            newUser = gansoUserFunctions.createUserInfo(gansoUser, gansoPwd, ip1, ip2, ip3, ip4, port, onosUser, onosPwd)
            errorLabel = gansoUserFunctions.errorNewUser(newUser) 

            textLabel.destroy()
            textLabel = tk.Label(self, text=errorLabel)
            textLabel.grid(row=6, column=3,columnspan=8, sticky="w")

            if newUser == 0:
                userInfo = gansoUserFunctions.getUserInfo(gansoUser)
                
                global GANSO_USR, ONOS_URL, ONOS_USR, ONOS_PWD, SWITCHES
                GANSO_USR = userInfo[0]
                ONOS_URL  = userInfo[2]
                ONOS_USR  = userInfo[3]
                ONOS_PWD  = userInfo[4]

                SWITCHES   = gansoNetworkFunctions.getSwitches(ONOS_URL, ONOS_USR, ONOS_PWD)

                controller.show_frame(PageMainMenu)

# ================================================================================================================================== #

# Main menu page - Allows user to go to pages: Network information, Controller configuration & Network Slice
class PageMainMenu(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        # Page description
        pageTitle = tk.Label(self, text = "Main Menu", font = LARGE_FONT)
        pageTitle.grid(row=0, column=0,columnspan=7)
        netInfoIcon = tk.PhotoImage(file="Resources\\Images\\netInfoIcon.png")
        contInfoIcon = tk.PhotoImage(file="Resources\\Images\\contInfoIcon.png")
        netSliceIcon = tk.PhotoImage(file="Resources\\Images\\netSliceIcon.png")

        # Button: Network information
        buttonNetInfo = ttk.Button(self, image=netInfoIcon, command=lambda: controller.show_frame(PageNetInfo))
        buttonNetInfo.image = netInfoIcon
        buttonNetInfo.grid(row=2,column=1)
        tk.Label(self, text="Network", font='arial 10 bold').grid(row=3,column=1)

        # Button: Controller configuration
        buttonOnosConfig = ttk.Button(self, image=contInfoIcon, command=lambda: controller.show_frame(PageController))
        buttonOnosConfig.image = contInfoIcon        
        buttonOnosConfig.grid(row=2, column=3)
        tk.Label(self, text="Controller", font='arial 10 bold').grid(row=3,column=3)

        # Button: Network Slice
        buttonNetSlice = ttk.Button(self, image=netSliceIcon, command=lambda: controller.show_frame(PageNetSlice))
        buttonNetSlice.image = netSliceIcon
        buttonNetSlice.grid(row=2, column=5)
        tk.Label(self, text="Network Slice", font='arial 10 bold').grid(row=3,column=5)

        # Action buttons
        buttonHelp = ttk.Button(self, text="Help",width=9, command=lambda: gansoMiscFunctions.help("MainMenu"))
        buttonHelp.grid(row=6,column=1,sticky="s")
        buttonLogOut = ttk.Button(self, text="Logout",width=9, command=lambda: controller.show_frame(PageLogin))
        buttonLogOut.grid(row=6,column=5,sticky="s")

        # GUI formatting
        tk.Label(self, text=" ",width=8).grid(row=1,column=0)
        tk.Label(self, text=" ",width=7).grid(row=2,column=2)
        tk.Label(self, text=" ",width=7).grid(row=2,column=4)
        tk.Label(self, text=" ",width=7).grid(row=2,column=6)     
        self.grid_rowconfigure(0, minsize=45)
        self.grid_rowconfigure(4, minsize=30)

# ================================================================================================================================== #

# Network Information page: Shows information of elements of user's network
class PageNetInfo(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        # Page description
        pageTitle = tk.Label(self, text = "    Network information", font = LARGE_FONT)
        pageTitle.grid(row=0, column=0,columnspan=7)
        switchInfoIcon = tk.PhotoImage(file="Resources\\Images\\switchInfoIcon.png")
        hostInfoIcon = tk.PhotoImage(file="Resources\\Images\\hostInfoIcon.png")
        linkInfoIcon = tk.PhotoImage(file="Resources\\Images\\linkInfoIcon.png")
        topoInfoIcon = tk.PhotoImage(file="Resources\\Images\\topoInfoIcon.png")
        clusterInfoIcon = tk.PhotoImage(file="Resources\\Images\\clusterInfoIcon.png")
        configInfoIcon = tk.PhotoImage(file="Resources\\Images\\configInfoIcon.png")

        # Show device information
        buttonSwitches = ttk.Button(self, image=switchInfoIcon, width=5, command=lambda: gansoNetworkFunctions.showNetInfo("devices", SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonSwitches.image = switchInfoIcon        
        buttonSwitches.grid(row=1, column=1)
        tk.Label(self, text="Switches", font='arial 10 bold').grid(row=2,column=1)

        # Show host information
        buttonHosts = ttk.Button(self, image=hostInfoIcon, width=5, command=lambda: gansoNetworkFunctions.showNetInfo("hosts", SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonHosts.image = hostInfoIcon
        buttonHosts.grid(row=1,column=3)
        tk.Label(self, text="Hosts", font='arial 10 bold').grid(row=2,column=3)

        # Show link information
        buttonLinks = ttk.Button(self, image=linkInfoIcon, width=5, command=lambda: gansoNetworkFunctions.showNetInfo("links", SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonLinks.image = linkInfoIcon
        buttonLinks.grid(row=1, column=5)
        tk.Label(self, text="Links", font='arial 10 bold').grid(row=2,column=5)

        # Show topology information
        buttonTopo = ttk.Button(self, image=topoInfoIcon, width=5, command=lambda: gansoNetworkFunctions.showNetInfo("topology", SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonTopo.image = topoInfoIcon        
        buttonTopo.grid(row=3, column=1)
        tk.Label(self, text="Topology", font='arial 10 bold').grid(row=4,column=1)

        # Show cluster information
        buttonCluster = ttk.Button(self, image=clusterInfoIcon, width=5, command=lambda: gansoNetworkFunctions.showNetInfo("cluster", SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonCluster.image = clusterInfoIcon
        buttonCluster.grid(row=3,column=3)
        tk.Label(self, text="Cluster", font='arial 10 bold').grid(row=4,column=3)

        # Show configuration information
        buttonConfig = ttk.Button(self, image=configInfoIcon, width=5, command=lambda: gansoNetworkFunctions.showNetInfo("configuration", SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonConfig.image = configInfoIcon
        buttonConfig.grid(row=3, column=5)
        tk.Label(self, text="Configuration", font='arial 10 bold').grid(row=4,column=5)

        # Action buttons
        buttonHelp = ttk.Button(self, text="Help",width=9, command=lambda:gansoMiscFunctions.help("NetworkInfo"))
        buttonHelp.grid(row=7,column=1,sticky="s")
        buttonBack = ttk.Button(self, text="<< Back",width=9, command=lambda:controller.show_frame(PageMainMenu))
        buttonBack.grid(row=7,column=5,sticky="s")

        # GUI formatting
        tk.Label(self, text=" ",width=12).grid(row=1,column=0)
        tk.Label(self, text=" ",width=9).grid(row=2,column=2)
        tk.Label(self, text=" ",width=7).grid(row=3,column=4)
        tk.Label(self, text=" ",width=7).grid(row=6,column=6)     
        self.grid_rowconfigure(0, minsize=50)

# ================================================================================================================================== #
#                                            Page: Controller                                             #
class PageController(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        pageTitle = tk.Label(self, text = "Controller information", font = LARGE_FONT)
        pageTitle.grid(row=0, column=0, columnspan=9)

        pageInfo = tk.Label(self, text="Choose information about:")
        pageInfo.grid(row=1, column=1, sticky="w", columnspan=4)
        
        tk.Label(self, text="",width=5).grid(row=1,column=0)

        buttonHosts = ttk.Button(self, text="Flows", width=10, command=lambda: gansoNetworkFunctions.showControllerInfo("flows", entryId.get(), SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonHosts.grid(row=2,column=1, sticky="w")

        buttonSwitches = ttk.Button(self, text="Intents", width=10, command=lambda: gansoNetworkFunctions.showControllerInfo("intents", entryId.get(), SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonSwitches.grid(row=2,column=2, sticky="w")
   
        buttonLinks= ttk.Button(self, text="Apps", width=10, command=lambda: gansoNetworkFunctions.showControllerInfo("applications", entryId.get(), SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonLinks.grid(row=2,column=3, sticky="w")
        
        buttonHelp= ttk.Button(self, text="Help", width=10, command=lambda: gansoMiscFunctions.help("Controller"))
        buttonHelp.grid(row=6,column=1, sticky="sw")

        tk.Label(self, text="Element Id (empty for ALL): ").grid(row=1,column=5,sticky="w",columnspan=4)
        entryId = ttk.Entry(self, width=24)
        entryId.grid(row=2, column=5,sticky="w", columnspan=3)

        tk.Label(self, text="", width=2).grid(row=1,column=4,sticky="w")

        tk.Label(self, text="", width=10).grid(row=4,column=5,sticky="w")
        tk.Label(self, text="", width=10).grid(row=5,column=5,sticky="w")

        buttonBack = ttk.Button(self, text="<< Back", command=lambda: controller.show_frame(PageMainMenu))
        buttonBack.grid(row=6,column=6,sticky="sw")
        buttonExit = ttk.Button(self, text="Exit", command=exit)
        buttonExit.grid(row=6,column=7,sticky="sw")
        
        self.grid_rowconfigure(0, minsize=50)
        self.grid_rowconfigure(1, minsize=30)
        self.grid_rowconfigure(2, minsize=30)
        self.grid_rowconfigure(3, minsize=10)
        self.grid_rowconfigure(4, minsize=30)
        self.grid_rowconfigure(5, minsize=50)

# ================================================================================================================================== #

# Network Slice Page - Allows user to create or upload network slices
class PageNetSlice(tk.Frame):

    def __init__(self, parent, controller):         

        tk.Frame.__init__(self, parent)

        # Page description
        pageTitle = tk.Label(self, text = "Network slice", font = LARGE_FONT)
        pageTitle.grid(row=0, column=0,columnspan=7)
        newGstIcon = tk.PhotoImage(file="Resources\\Images\\newGstIcon.png")
        uploadGstIcon = tk.PhotoImage(file="Resources\\Images\\uploadGstIcon.png")
        viewSlicesIcon = tk.PhotoImage(file="Resources\\Images\\viewSlicesIcon.png")

        # Create GST
        buttonNewGst = ttk.Button(self, image=newGstIcon, width=10, command=lambda: gansoNetworkFunctions.newGst(GANSO_USR, SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonNewGst.image = newGstIcon
        buttonNewGst.grid(row=2, column=1)
        tk.Label(self, text="New slice", font='arial 10 bold').grid(row=3,column=1)

        # Upload NEST
        buttonUpload = ttk.Button(self, image=uploadGstIcon, width=10, command=lambda: uploadGST(SWITCHES, ONOS_URL, ONOS_USR, ONOS_PWD))
        buttonUpload.image = uploadGstIcon
        buttonUpload.grid(row=2,column=3)
        tk.Label(self, text="Upload NEST", font='arial 10 bold').grid(row=3,column=3)

        # Show created slices
        showSlices = ttk.Button(self, image=viewSlicesIcon, width=10, command=lambda: gansoNetworkFunctions.showSlices())
        showSlices.image = viewSlicesIcon
        showSlices.grid(row=2, column=5)
        tk.Label(self, text="View slices", font='arial 10 bold').grid(row=3,column=5)

        # Action buttons
        buttonHelp = ttk.Button(self, text="Help",width=9, command=lambda:gansoMiscFunctions.help("NetworkSlice"))
        buttonHelp.grid(row=6,column=1,sticky="s")
        buttonBack = ttk.Button(self, text="<< Back",width=9, command=lambda:controller.show_frame(PageMainMenu))
        buttonBack.grid(row=6,column=5,sticky="s")

        # GUI formatting
        tk.Label(self, text=" ",width=8).grid(row=1,column=0)
        tk.Label(self, text=" ",width=7).grid(row=2,column=2)
        tk.Label(self, text=" ",width=7).grid(row=2,column=4)
        tk.Label(self, text=" ",width=7).grid(row=2,column=6)     
        self.grid_rowconfigure(0, minsize=45)
        self.grid_rowconfigure(4, minsize=30)
        
        def uploadGST(switches, onosUrl, onosUsr, onosPwd):
            self.filename = filedialog.askopenfilename(initialdir=".", title="Select the GST", \
                filetypes=(("xml files", "*.xml"),("json files", "*.json")))

            if self.filename != '':
                gansoNetworkFunctions.createNetworkSlice(self.filename, switches, onosUrl, onosUsr, onosPwd, True)


app = GansoApp()

app.mainloop()