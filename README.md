# Ender-3-Easy-Extras
This program does lots of cool stuff! You can easily add manual filament change code to your gcode file or set up your printer to draw things with a pen based off Easel

#-------------------------------3d Post-Processing Window---------------------------#
To use this window, first import your already sliced gcode file. Simply set the slider to the layer you want to insert code, and click on an insert button.
The inserts available are:
-Manual chainge filament (must have this enabled in printers firmware to work: https://marlinfw.org/docs/gcode/M600.html)


#--------------------------------Pen Plotting Window---------------------------------#
I made this python program that takes gcode from easel and converts it to work with the Ender 3. Right now the program is setup for pen plotting. THIS IS NOT FINISHED. NOT MY FAULT IF YOUR PRINTER BREAKS FROM THIS.

To use: open Easel: https://easel.inventables.com
Make a new project
Click on Machine and then set the Work area X and Y to 235mm
Next select material size and set X and Y to 234.9mm and Z thickness to 1mm
Select Cut Settings and set Feed Rate to what ever you want. I recommend 700mm/m for starting off.
Set Plunge Rate to 50.0mm/m
Set Depth Per Pass to 1mm
Finally import your designing into Easel, set the cut depth of the model to 1mm. To do this, click on the object you added and select Cut and drag the slider to 1mm.
Go to Machine, click advanced settings, and hit Generate Gcode. Then Export Gcode and save it somewere.

In my program, edit the python file and chainge the penOffsetX, penOffsetY, penOffsetZ variables to the offset of pen tip from the hottend nozzle. ![IMG_1818](https://user-images.githubusercontent.com/42445164/117326518-b9f68880-ae5f-11eb-9351-b19b145085ac.JPG)
![IMG_1817](https://user-images.githubusercontent.com/42445164/117326525-bb27b580-ae5f-11eb-88c3-e622289561df.JPG)

Finally run the program with python3 
In the program, you can select the Easel file and also use the slider to set a Z offset (usually set this to 0).
Finally hit run. The program will make a new .gcode file where the old file was located. Move this to the 3d printers sd card and run!


