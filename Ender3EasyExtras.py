from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from pathlib import Path
import shutil
import os
import re
import time

#Set these values to mach your settings
penOffsetZ = 11.0 #pen is 16mm below nozzle.
penOffsetX = -44.5 #pen is 43mm to the left of the hottend when looking at printer head on.
penOffsetY = -32 #pen is 26mm toward me when I stand looking streight at the front of the printer.
printerMaxX = 235 #3d printer bed blate size
printerMaxY = 235 #3d printer bed blate size
penSafetyHeight = 5 #use this value to set the height the pen will go up when not activaly drawing
CuraFirstLayerThickness = 0.18 #The thickness of the first layer in your print


#CNC DO NOT CHAINGE
EaselSaftyHeight = 16
fileFound=False
fileFoundGcode = False
targetFileDirGcode = "/"
targetFileDir = "/"
homeDir = str(Path.home())
printHeight = 0 # DO NOT CHAINGE Set to 0
toolChaingeState = True
BLstate = True
layerThickness = 0.24 # NOT IN USE
maxLayerNum = 0

"""
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
    PrintWindow.geometry("500x300")

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
        i=0
        for line in f_old:
            f_new.write(line)
            if (';LAYER:' + str(i) in line) and (i <= printSlider.get()):
                f_new.write("M117 Filament Chainge in: " + str(printSlider.get() - i) + "\n") 
                i+=1
                print(i)
            if ';LAYER:' + str(printSlider.get()) + "\n" == line:
                f_new.write("M600\n")

def updatePrint(event):
    global printSlider
    global print_chaingefilament
    #print("updating: " + str(printSlider.get()))
    print_chaingefilament.config(text="Insert Filament Chainge at: " + str(printSlider.get()))

"""
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

def browseGcodeFile():
    filename = filedialog.askopenfilename(initialdir = homeDir, title = "Select File",filetypes = (("all files","*.*"),("Gcode files","*.gcode")))
    #label_file_explorer.configure(text="File Opened: "+filename, fg="white")
    #print(filename)
    global targetFileDirGcode
    global fileFoundGcode
    global maxLayerNum
    if not filename:
        print("no file selected")
        fileFoundGcode = False
    else:
        targetFileDirGcode = filename
        print(targetFileDir)
        fileFoundGcode = True
        fG = open(targetFileDirGcode)
        textFG = fG.read()
        tmpCounter = 0
        for lineT in textFG.split('\n'):
            txt = ";LAYER:" + str(tmpCounter)
            if txt in lineT:
                print(tmpCounter)
                tmpCounter += 1
        maxLayerNum = tmpCounter
        sli1.configure(from_=tmpCounter)

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

def runProgramStandalone():
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
            print("adding bltouch code")
        else:
            textF = str("G28\n") + textF
        beginToolCode = ""
        if toolChaingeState:
            #re.sub('G90\n', str(StartToolChaingeCode.get(1.0, "end-1c")) + "\n", textF)
            #print (str(StartToolChaingeCode.get(1.0, "end-1c")) + "\n")
            beginToolCode = str(StartToolChaingeCode.get(1.0, "end-1c")) + "\n"
            index = textF.find("G1")
            print(index)
            textF = textF[:index] + beginToolCode + textF[index:]

            #index = textF.find("G21\n")
            textF = textF + "\n" + str(EndToolChaingeCode.get(1.0, "end-1c")) + "\n" + "G91 ;Relative positioning\nG1 E-2 F2700 ;Retract a bit\nG1 E-2 Z0.2 F2400 ;Retract and raise Z\nG1 X5 Y5 F3000 ;Wipe out\nG1 Z10 ;Raise Z more\nG90 ;Absolute positioning\nG1 X0 Y50 ;Present print\nM106 S0 ;Turn-off fan\nM104 S0 ;Turn-off hotend\nM140 S0 ;Turn-off bed\nM84 X Y E ;Disable all steppers but Z"
        #else:
            #print("NICK ADD G4 P10000 command here in gcode to wate 10 seconds")
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
                    if (float(dta[1]) <= (penOffsetZ + printHeight)):
                        textF = textF.replace(li, "G1 Z" + str(penOffsetZ + printHeight) + " F" + str(dta[2]) + "\n")

                if 'G0 Z' in li:
                    dta = re.findall('\d*\.?\d+',li)
                    if (float(dta[1]) <= (penOffsetZ + printHeight)):
                        textF = textF.replace(li, "G0 Z" + str(penOffsetZ + printHeight) + " F" + str(dta[2]) + "\n")
        f.close()
        f = open(dirname + "/" + curntName + ".gcode", "w")
        if stillGoodToGo:
            f.write(textF)
            print(textF)
            #label_file_explorer.configure(text="DONE", fg="white")
        else:
            print("Error in code")
            #label_file_explorer.configure(text="error, probulby gcode tried to run toolhead out of bounds")
        

def runProgramMix():
    global CuraFirstLayerThickness
    global EaselSaftyHeight
    global penSafetyHeight
    global maxLayerNum
    global fileFoundGcode
    global fileFound
    global targetFileDir
    global targetFileDirGcode
    global printHeight
    global toolChaingeState
    global layerThickness
    global BLstate
    if fileFound and fileFoundGcode:
        stillGoodToGo=True
        dirname, fname = os.path.split(targetFileDir)
        curntName, extensionName = fname.split(".")

        dirnameGcode, fnameGcode = os.path.split(targetFileDirGcode)
        curntNameGcode, extensionNameGcode = fnameGcode.split(".")
        #shutil.move(targetFileDir, dirname + "/" + curntName + ".gcode")
        #shutil.copy( dirname + "/" + curntName + ".gcode", targetFileDir)
        f = open(dirname + "/" + curntName + ".nc")
        textF = f.read()

        fG = open(targetFileDirGcode)
        textFG = fG.read()

        tmpCounter = 0
        layerT = 0
        for lineT in textFG.split('\n'):
            txt = ";LAYER:" + str(tmpCounter)
            if txt in lineT:
                print(tmpCounter)
                tmpCounter += 1
            if ";Layer height: " in lineT:
                first, second, third = lineT.split(' ')
                #print(first)
                #print(second)
                #print(float(str(third)))
                #printHeight = tmpCounter * float(str(third))
                layerT = float(third)
                print(third)
        if sli1.get() == 1:
            printHeight = CuraFirstLayerThickness
        elif sli1.get() > 1:
            printHeight = CuraFirstLayerThickness + ((sli1.get() - 1) * layerT)
        print(layerThickness)
        #printHeight = sli1.get() * layerT
        print(printHeight)

        

        beginToolCode = ""
        if toolChaingeState:
            beginToolCode = str(StartToolChaingeCode.get(1.0, "end-1c")) + "\n"
            textF = beginToolCode + textF
            textF = textF + "\n" + str(EndToolChaingeCode.get(1.0, "end-1c")) + "\n"
        else:
            print("NICK ADD G4 P10000 command here in gcode to wate 10 seconds")
        #printHeight = sli1.get()
        with open(dirname + "/" + curntName + ".nc") as l:
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
                    if (float(dta[1]) <= (penOffsetZ + printHeight)):
                        textF = textF.replace(li, "G1 Z" + str(penOffsetZ + layerT + printHeight) + " F" + str(dta[2]) + "\n")
                    if (float(dta[1]) >= (EaselSaftyHeight)):
                        textF = textF.replace(li, "G1 Z" + str(penOffsetZ + printHeight + layerT + penSafetyHeight) + " F" + str(dta[2]) + "\n")

                if 'G0 Z' in li:
                    dta = re.findall('\d*\.?\d+',li)
                    if (float(dta[1]) <= (penOffsetZ + printHeight)):
                        textF = textF.replace(li, "G0 Z" + str(penOffsetZ + printHeight + layerT) + " F" + str(dta[2]) + "\n")
                    if (float(dta[1]) <= (EaselSaftyHeight)):
                        textF = textF.replace(li, "G0 Z" + str(penOffsetZ + printHeight + layerT + penSafetyHeight) + " F" + str(dta[2]) + "\n")
        f.close()
        #f = open(dirname + "/" + curntName + ".gcode", "w")
        if stillGoodToGo:
            #f.write(textF)
            #print(textF)
            if sli1.get() < maxLayerNum:
                Newindex = textFG.find(";LAYER:" + str(sli1.get()) + "\n")
                print(Newindex)
                #returnToHeight = printHeight + LayerThickness
                # FIx problem with hottend not returning to current print height
                final_string = textFG[:Newindex] + ";Ender easy system inserted code\n" + textF + "G1 X117.5 Y117.5 F500\n G1 Z" + str(printHeight + layerT) + " F500\n" + textFG[Newindex:]
                ff = open(dirname + "/" + curntNameGcode + "CNCMix.gcode", "w")
                ff.write(final_string)
                window.destroy()
                time.sleep(0.5)
            elif sli1.get() == maxLayerNum:
                Newindex = textFG.find("G91 ;Relative positioning\n")
                print(Newindex)
                final_string = textFG[:Newindex] + ";Ender easy system inserted code\n" + textF + textFG[Newindex:]
                ff = open(dirname + "/" + curntNameGcode + "CNCMix.gcode", "w")
                ff.write(final_string)
                window.destroy()
                time.sleep(0.5)
                
            #label_file_explorer.configure(text="DONE", fg="white")
        else:
            print("Error in code")
            #label_file_explorer.configure(text="error, probulby gcode tried to run toolhead out of bounds")
        

def runProgramCheck():
    print(sli1.get())
    if sli1.get() == 0:
        print("running standalone cnc")
        runProgramStandalone()
    elif sli1.get() > 0:
        print("mixing cnc with cura gcode")
        runProgramMix()
                                                                                                  
# Create the root window
window = Tk()
  
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")

# Set window title
window.title('Nicks Ender 3 CNC Customizer')
  
# Set window size
window.geometry("800x500")

#Set window background color
window.config(background = "gray") #white
# Create a File Explorer label



#frame = Frame(window,
#       border=1,
#        relief=GROOVE,
#        background="blue",
#    )

offsetLabel = Label(window, text="Insert Cnc code to run after layer", bg="gray", fg="white")
offsetLabel.grid(column=0,row=0, sticky=S, pady=0)

button_exploreGcode = Button(window,text = "Browse Gcode",command = browseGcodeFile, bg="white")
button_exploreGcode.grid(column = 0, row = 1)

sli1 = Scale(window, from_=50, to=0, tickinterval=0.1, orient=VERTICAL, bg = "RED") #RED
sli1.grid(pady=10,padx=5, sticky=S+N, rowspan=10)

#toolChaingeCodeText = StringVar()
StartToolChaingeLabel = Label(window, text="Begining tool chainge code", bg="gray", fg="white")
StartToolChaingeLabel.grid(column=1,row=0, sticky=S, pady=10)

StartToolChaingeCode = ScrolledText(window, width = 15, height=7)
StartToolChaingeCode.grid(column=1,row=1, sticky=N, rowspan=2)

EndToolChaingeLabel = Label(window, text="End tool chainge code", bg="gray", fg="white")
EndToolChaingeLabel.grid(column=1,row=3, sticky=NS)

EndToolChaingeCode = ScrolledText(window, width = 15, height=7)
EndToolChaingeCode.grid(column=1,row=4, sticky=N, rowspan=2)

toolSave = Button(window, text="Save Tool Chainge", command=saveToolCode)
toolSave.grid(column=1,row=6)

descriptionLable = Label(window,text = "To use this program, export a toolpath from easel with:\nPlunge Rate: 50mm/m\nDepth per pass: 1mm\nMaterial size: 235mm by 235mm by 1mm\nSafety Height: 16 or heigher\n",fg = "white", bg="gray")
descriptionLable.grid(column = 2, row = 0, pady=10)

#label_file_explorer = Label(window,text = "",fg = "white")
#label_file_explorer.grid(column = 2, row = 1)

button_explore = Button(window,text = "Browse Files",command = browseFiles, bg="white")
button_explore.grid(column = 2, row = 1)

toolLable = Label(window,text = "Use Auto Toolchainger",fg = "white", bg="gray")
toolLable.grid(column=2,row=2)

tool_button = Button(window, image = on, bd = 0, command = toolChaingeSwitch)
tool_button.grid(column = 2, row = 3, pady=2)

BLlabel = Label(window,text = "BL-Touch Homing",fg = "white", bg="gray")
BLlabel.grid(column = 2, row = 4)

BL_button = Button(window, image = on, bd = 0, command = BLSwitch)
BL_button.grid(column = 2, row = 5, pady=2)

button_run = Button(window,text = "Run",command = runProgramCheck, bg="white")
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
#sli1.grid_remove()
#offsetLabel.grid_remove()
#label_file_explorer.grid_remove()
toolChaingeSwitch()
toolChaingeSwitch()
#open3d()

# Let the window wait for any events
window.mainloop()
#PrintWindow.mainloop()

#For drawing on 3d print, read ;Layer height: 0.__ value
#Read ;MAXZ:_.___ value
# Read ;LAYER:_ for layer number !!!
