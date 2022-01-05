import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

# Global variables
LARGE_FONT   =  ("Verdana", 12, 'bold')
BUTTON_FONT  = ("Arial", 10, 'bold')

# Function to show a page's help text
def help(whichHelp):

    helpBox = tk.Toplevel()

    if whichHelp == "MainMenu":
        labelText = "Main menu"
    elif whichHelp == "NetworkInfo":
        labelText = "Network information"
    elif whichHelp == "Login":
        labelText = "Login"
    elif whichHelp == "NewUser":
        labelText = "New user"
    elif whichHelp == "Controller":
        labelText = "Controller"
    elif whichHelp == "NetworkSlice":
        labelText = "Network Slice"

    # Scrollbars
    scrollbarVer = ttk.Scrollbar(helpBox)
    scrollbarVer.pack(side = "right", fill = "y")
    scrollbarHor = ttk.Scrollbar(helpBox, orient=tk.HORIZONTAL)
    scrollbarHor.pack(side = "bottom", fill = "x")

    tk.Label(helpBox, text=labelText + " page help", font = LARGE_FONT, height=2).pack()
    info = tk.Text(helpBox,yscrollcommand=scrollbarVer.set, xscrollcommand=scrollbarHor.set,wrap="none")
    info.pack(expand="yes",fill=tk.BOTH)

    scrollbarVer.config(command=info.yview)
    scrollbarHor.config(command=info.xview)

    help_file = Path("./resources/Help/help"+whichHelp + ".txt")

    file = open(help_file)
    info.insert(1.0, file.read())

# ================================================================================================================================== #

def outputFolder(title='Select output folder'):
            
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    folder_path = filedialog.askdirectory()
    return folder_path