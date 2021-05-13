from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from pathlib import Path
import shutil
import os
import re

penOffsetZ = 13.5 #pen is 16mm below nozzle.
penOffsetX = -47 #pen is 43mm to the left of the hottend when looking at printer head on.
penOffsetY = -30 #pen is 26mm toward me when I stand looking streight at the front of the printer.
printerMaxX = 235
printerMaxY = 235

#CNC
fileFound=False
targetFileDir = "/"
homeDir = str(Path.home())
printHeight = 2
toolChaingeState = True
BLstate = True

#3d print
PrintWindow=None
printFile = "/"
printSlider=None
print_chaingefilament=None

#####################----3d print editing-----###################
def open3d():
    global PrintWindow
    global printSlider
    global print_chaingefilament
    PrintWindow=Toplevel(window)
    PrintWindow.title("3d printing tool")
    PrintWindow.geometry("800x500")

    printLabel = Label(PrintWindow, text="Here you can post process gcode from cura.")
    printLabel.grid(column=2,row=0, sticky=S, pady=0)

    print_explore = Button(PrintWindow,text = "Browse gcode",command = browsePrintFile, bg="white")
    print_explore.grid(column = 2, row = 1)

    printSlider = Scale(PrintWindow, from_=50, to=0, tickinterval=0.1, orient=VERTICAL, bg = "RED")
    printSlider.grid(pady=10,padx=10, sticky=S+N, rowspan=3)#, column=1, row=13)

    print_chaingefilament = Button(PrintWindow,text = "Chainge Filament at: 0",command = chaingeFilament, bg="white")
    print_chaingefilament.grid(column = 2, row = 3)

    printSlider.bind('<ButtonRelease>',updatePrint)

def browsePrintFile():
    global PrintWindow
    global printFile
    global printSlider
    filename = filedialog.askopenfilename(initialdir = homeDir, title = "Select File",filetypes = (("all files","*.*"),("Gcode files","*.gcode")))
    if not filename:
        print("no file selected")
    else:
        printFile = filename
        findTxt = False
        with open(printFile) as temp_f:
            datafile = temp_f.readlines()
        i=0
        for line in datafile:
            if (';LAYER:' + str(i)) in line:
                i+=1
                #print("found layer: " + str(i))
        #print("working: " + str(i))
        printSlider.config(from_=i)

def chaingeFilament():
    global printSlider
    global printFile
    print("chainging filament at layer: " + str(printSlider.get()))
    dirname, fname = os.path.split(printFile)
    curntName, extensionName = fname.split(".")
    with open(printFile) as f_old, open(dirname + "/" + curntName + "Modified." + extensionName, "w") as f_new:
        for line in f_old:
            f_new.write(line)
            if ';LAYER:' + str(printSlider.get()) in line:
                f_new.write("M900\n")

def updatePrint(event):
    global printSlider
    global print_chaingefilament
    #print("updating: " + str(printSlider.get()))
    print_chaingefilament.config(text="Insert Filament Chainge at: " + str(printSlider.get()))


################################-----CNC-----##################

def toolChaingeSwitch():
    global toolChaingeState
    if toolChaingeState:
        tool_button.config(image = off)
        print("off")
        toolChaingeState = False
        #sli1.grid_remove()
        #offsetLabel.grid_remove()
    else:  
        tool_button.config(image = on)
        print("on")
        toolChaingeState = True
        #sli1.grid(pady=10,padx=5, sticky=S+N, rowspan=10)
        #offsetLabel.grid(column=0,row=0, sticky=S, pady=0)

def BLSwitch():
    global BLstate
    if BLstate:
        BL_button.config(image = off)
        print("Bl touch off")
        BLstate = False
        #sli1.grid_remove()
        #offsetLabel.grid_remove()
    else:  
        BL_button.config(image = on)
        print("BL touch on")
        BLstate = True
        #sli1.grid(pady=10,padx=5, sticky=S+N, rowspan=10)
        #offsetLabel.grid(column=0,row=0, sticky=S, pady=0)
        
  
# Function for opening the
# file explorer window

def saveToolCode():
    txt = open("StartToolChaingeCode.txt", "w+")
    txt.write(StartToolChaingeCode.get(1.0, "end-1c"))
    txt.close()

    txt = open("EndToolChaingeCode.txt", "w+")
    txt.write(EndToolChaingeCode.get(1.0, "end-1c"))
    txt.close()

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = homeDir, title = "Select File",filetypes = (("all files","*.*"),("NC files","*.nc")))
    #label_file_explorer.configure(text="File Opened: "+filename, fg="white")
    #print(filename)
    global targetFileDir
    global fileFound
    if not filename:
        print("no file selected")
        fileFound = False
    else:
        targetFileDir = filename
        #print(targetFileDir)
        fileFound = True

def edit_string(stringC):
    findTxt = False
    with open(stringC) as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if 'G1 Z-1.000 F50.0' in line:
            findTxt = True
            return True
    if not findTxt:
        #label_file_explorer.configure(text="File incorrectly formated, Please set Z feedrate to 50mm and Cut Depth to 1mm", fg="white")
        return False
    #return False  # The string does not exist in the file

def runProgram():
    global fileFound
    global targetFileDir
    global printHeight
    global toolChaingeState
    global BLstate
    if fileFound:
        stillGoodToGo=True
        dirname, fname = os.path.split(targetFileDir)
        curntName, extensionName = fname.split(".")
        shutil.move(targetFileDir, dirname + "/" + curntName + ".gcode")
        #shutil.copy( dirname + "/" + curntName + ".gcode", targetFileDir)
        f = open(dirname + "/" + curntName + ".gcode")
        textF = f.read()
        if BLstate:
            textF = str("G28\nM420 S1\nG29\n") + textF
        else:
            textF = str("G28\n") + textF
        if toolChaingeState:
            re.sub('G90\n', str(StartToolChaingeCode.get(1.0, "end-1c")) + "\n", textF)
        else:
            print("NICK ADD G4 P10000 command here in gcode to wate 10 seconds")
        #print(textF)
        #printHeight = sli1.get()
        #if(edit_string(dirname + "/" + curntName + ".gcode")):
         #   textF = textF.replace("G1 Z-1.000 F50.0", "G1 Z" + str(printHeight + penOffsetZ) + " F150.0")
        with open(dirname + "/" + curntName + ".gcode") as l:
            datline = l.readlines()
        for li in datline:
                if 'G1 X' in li:
                    dta = re.findall('\d*\.?\d+',li)
                    if ((round(float(dta[1]) - penOffsetX, 3) >= penOffsetX * -1) and (round(float(dta[1]) - penOffsetX, 3) <= printerMaxX)):
                        if ((round(float(dta[2]) - penOffsetY, 3) >= penOffsetY * -1) and (round(float(dta[2]) - penOffsetY, 3) <= printerMaxY)):
                            #print("value bad, goes out of range")
                            print("good Value")
                        else:
                            stillGoodToGo = False
                    else:
                        stillGoodToGo = False
                    textF = textF.replace(li, "G1 X" + str(round(float(dta[1]) - penOffsetX, 3)) + " Y" + str(round(float(dta[2]) - penOffsetY, 3)) + " F" + dta[3] + "\n")

                if 'G0 X' in li:
                    dta = re.findall('\d*\.?\d+',li)
                    if ((round(float(dta[1]) - penOffsetX, 3) >= penOffsetX * -1) and (round(float(dta[1]) - penOffsetX, 3) <= printerMaxX)):
                        if ((round(float(dta[2]) - penOffsetY, 3) >= penOffsetY * -1) and (round(float(dta[2]) - penOffsetY, 3) <= printerMaxY)):
                            #print("value bad, goes out of range")
                            print("good Value")
                        else:
                            stillGoodToGo = False
                    else:
                        stillGoodToGo = False
                    textF = textF.replace(li, "G0 X" + str(round(float(dta[1]) - penOffsetX, 3)) + " Y" + str(round(float(dta[2]) - penOffsetY, 3)) + " F800\n")
                
                if 'G1 Z' in li:
                    dta = re.findall('\d*\.?\d+',li)
                    if (float(dta[1]) <= (penOffsetZ - printHeight)):
                        textF = textF.replace(li, "G1 Z" + str(penOffsetZ - printHeight) + " F" + str(dta[2]) + "\n")

                if 'G0 Z' in li:
                    dta = re.findall('\d*\.?\d+',li)
                    if (float(dta[1]) <= (penOffsetZ - printHeight)):
                        textF = textF.replace(li, "G0 Z" + str(penOffsetZ - printHeight) + " F" + str(dta[2]) + "\n")
        f.close()
        f = open(dirname + "/" + curntName + ".gcode", "w")
        if stillGoodToGo:
            f.write(textF)
            print(textF)
            #label_file_explorer.configure(text="DONE", fg="white")
        else:
            print("Error in code")
            #label_file_explorer.configure(text="error, probulby gcode tried to run toolhead out of bounds")
        
                                                                                                  
# Create the root window
window = Tk()
  
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")

# Set window title
window.title('Nicks Ender 3 CNC Customizer')
  
# Set window size
window.geometry("800x500")

#Set window background color
#window.config(background = "white")
# Create a File Explorer label



#frame = Frame(window,
##        border=1,
 #       relief=GROOVE,
 #       background="blue",
 #   )

offsetLabel = Label(window, text="Pen printing offset")
offsetLabel.grid(column=0,row=0, sticky=S, pady=0)

sli1 = Scale(window, from_=50, to=0, tickinterval=0.1, orient=VERTICAL, bg = "RED")
sli1.grid(pady=10,padx=5, sticky=S+N, rowspan=10)

#toolChaingeCodeText = StringVar()
StartToolChaingeLabel = Label(window, text="Begining tool chainge code")
StartToolChaingeLabel.grid(column=1,row=0, sticky=S, pady=10)

StartToolChaingeCode = ScrolledText(window, width = 15, height=7)
StartToolChaingeCode.grid(column=1,row=1, sticky=N, rowspan=2)

EndToolChaingeLabel = Label(window, text="End tool chainge code")
EndToolChaingeLabel.grid(column=1,row=3, sticky=NS)

EndToolChaingeCode = ScrolledText(window, width = 15, height=7)
EndToolChaingeCode.grid(column=1,row=4, sticky=N, rowspan=2)

toolSave = Button(window, text="Save Tool Chainge", command=saveToolCode)
toolSave.grid(column=1,row=6)

descriptionLable = Label(window,text = "To use this program, export a toolpath from easel with:\nPlunge Rate: 50mm/m\nDepth per pass: 1mm\nMaterial size: 235mm by 235mm by 1mm\n",fg = "white")
descriptionLable.grid(column = 2, row = 0, pady=10)

#label_file_explorer = Label(window,text = "",fg = "white")
#label_file_explorer.grid(column = 2, row = 1)

button_explore = Button(window,text = "Browse Files",command = browseFiles, bg="white")
button_explore.grid(column = 2, row = 1)

toolLable = Label(window,text = "Use Auto ToolchaingerNOTWORKING",fg = "white")
toolLable.grid(column=2,row=2)

tool_button = Button(window, image = on, bd = 0, command = toolChaingeSwitch)
tool_button.grid(column = 2, row = 3, pady=2)

BLlabel = Label(window,text = "BL-Touch Homing",fg = "white")
BLlabel.grid(column = 2, row = 4)

BL_button = Button(window, image = on, bd = 0, command = BLSwitch)
BL_button.grid(column = 2, row = 5, pady=2)

button_run = Button(window,text = "Run",command = runProgram, bg="white")
button_run.grid(column = 2,row = 6)
  
print("Starting Program...")
try:
    txt = open("StartToolChaingeCode.txt", "r")
    StartToolChaingeCode.insert(1.0, txt.read())
    txt.close()
except:
    print("No Start Tool chainge code file to load")
try:
    txt = open("EndToolChaingeCode.txt", "r")
    EndToolChaingeCode.insert(1.0, txt.read())
    txt.close()
except:
    print("No End Tool chainge code file to load")
sli1.grid_remove()
offsetLabel.grid_remove()
#label_file_explorer.grid_remove()
toolChaingeSwitch()
open3d()

# Let the window wait for any events
window.mainloop()
PrintWindow.mainloop()

#For drawing on 3d print, read ;Layer height: 0.__ value
#Read ;MAXZ:_.___ value
# Read ;LAYER:_ for layer number !!!
