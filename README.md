# Lead_Automation use instructions

## Basic run
1) Open Command Prompt, enter "cd ~/Documents/Lead_Automation"
2) Open the remote XRF app. Log in, but do not click the collect sample icon.
3) In the Command Prompt, enter "python UnifiedRun.py"
4) The program will take several seconds to start. Once it has, the Command Prompt will ask if you want to home the system.
  a) If the gantry is not in the corner closest to the computer or this is the first use of the day, enter "y"
  b) Otherwise, enter "n"
5) The program will run automatically until it finishes or encounters an error. Do not move other windows in front of the XRF app, as the program needs to see it on screen to interact with it.

## Adjusting parameters
I plan on streamlining this so things are less scattered, but a rough map of things as they stand.
### Starting position
In ArduinoControl.py, at the top of the file, set xStart and yStart

### Center offset
In ArduinoControl.py, in function readLabels(), set xOffset and yOffset

# Lead_Automation programs
All the current code for AXLE, presented in rough order of dependency:

## UnifiedRun.py
The main wrapper for all the other programs, controls the pattern in which samples are read and transfers data between programs. Depends on **ArduinoControl.py**, **XRFControl.py**, and **GantryControl.py**

## ArduinoControl.py
Reads labels and tape for each sample, controls how that search is performed. Depends on **GantryControl.py** and **mk2Camera.py**

## mk2Camera.py
Controls the color of tape being searched for and the OCR for finding and reading labels.

## GantryControl.py
Performs raw communications with the motors

## XRFControl.py
Tracks the status of the XRF session. Depends on **mk2Auto.py**

## mk2Auto.py
Organizes XRF communications and error checking. Depends on **ButtonTask.py**

## ButtonTask.py
Performs raw communications with XRF GUI and results checking.
