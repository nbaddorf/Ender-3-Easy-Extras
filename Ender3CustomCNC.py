from tkinter import *
from tkinter import filedialog
from pathlib import Path
import shutil
import os
import re


fileFound=False
targetFileDir = "/"
homeDir = str(Path.home())
printHeight = 20
penOffsetZ = 2 #pen is 2mm below nozzle
penOffsetX = -43
penOffsetY = -26
printerMaxX = 235
printerMaxY = 235


  
# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = homeDir, title = "Select File",filetypes = (("all files","*.*"),("NC files","*.nc")))
    label_file_explorer.configure(text="File Opened: "+filename, fg="white")
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
        label_file_explorer.configure(text="File incorrectly formated, Please set Z feedrate to 50mm and Cut Depth to 1mm", fg="white")
        return False
    #return False  # The string does not exist in the file

def runProgram():
    global fileFound
    global targetFileDir
    global printHeight
    if fileFound:
        stillGoodToGo=True
        dirname, fname = os.path.split(targetFileDir)
        curntName, extensionName = fname.split(".")
        shutil.move(targetFileDir, dirname + "/" + curntName + ".gcode")
        #shutil.copy( dirname + "/" + curntName + ".gcode", targetFileDir)
        f = open(dirname + "/" + curntName + ".gcode")
        textF = f.read()
        textF = str("G28\nM420 S1\nG29\n") + textF
        #print(textF)
        printHeight = sli1.get()
        if(edit_string(dirname + "/" + curntName + ".gcode")):
            textF = textF.replace("G1 Z-1.000 F50.0", "G1 Z" + str(printHeight + penOffsetZ) + " F150.0")
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
        f.close()
        f = open(dirname + "/" + curntName + ".gcode", "w")
        if stillGoodToGo:
            f.write(textF)
            print(textF)
            label_file_explorer.configure(text="DONE", fg="white")
        else:
            label_file_explorer.configure(text="error, probulby gcode tried to run toolhead out of bounds")
        
                                                                                                  
# Create the root window
window = Tk()
  


# Set window title
window.title('Nicks Ender 3 CNC Customizer')
  
# Set window size
window.geometry("800x500")
  
#Set window background color
#window.config(background = "white")
# Create a File Explorer label
descriptionLable = Label(window,
                            text = "To use this program, export a toolpath from easel with:\nPlunge Rate: 50mm/m\nDepth per pass: 1mm\nMaterial size: 235mm by 235mm by 1mm\n",
                            width = 100, height = 4,
                            fg = "white")

label_file_explorer = Label(window,
                            text = "",
                            width = 100, height = 4,
                            fg = "white")

sli1 = Scale(window, from_=50, to=0, tickinterval=0.1, orient=VERTICAL, bg = "RED")
sli1.place(relx=0.15,rely=0.06,relwidth=0.05, relheight=0.8)

  
      
button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles, bg="white")
  
button_run = Button(window,
                     text = "Run",
                     command = runProgram, bg="white")
  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
descriptionLable.grid(column = 1, row = 1)
label_file_explorer.grid(column = 1, row = 2)
  
button_explore.grid(column = 1, row = 3)
#sli.grid(column = 1, row = 4)

button_run.grid(column = 1,row = 4)
  
# Let the window wait for any events
window.mainloop()
