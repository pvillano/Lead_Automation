# Lead_Automation use instructions

## Basic run
### Setup
1) Turn on the gantry by flipping the switch labeled "AC On" 
up. The green light labeled "DC Power" will turn on. 
2) Turn on the XRF by holding the power button down until the screen lights up.
3) Turn the camera's LED on by scrolling the wheel on its cable, next to the USB port.
4) Open the NDTr app on the computer. Once it has connected to the XRF, click accept and enter the passcode.
#### Desktop Icon
1) Find the icon labeled "AXLE_control". Double click it.
2) A black window will open, and after a pause, the user interface will open.
#### Command Line
1) Open Command Prompt, enter "cd ~/Documents/Lead_Automation"
2) In the Command Prompt, enter "python GUI.py". The user interface will open.
###Running samples
1) Before running the first sample of the day, home the XRF by pressing "Home". This will ensure the robot moves acurately.
2) Select the type of sample you wish to run. 
	a) If you have a small number of samples to run, enter that number in the box labeled "Samples"
	b) If you have a large batch, check the box labeled "Continuous mode"
3) Enter a memorable name in the field labeled "Run Name"
4) Click "Start" to run the samples. Click "Cancel" to reset all inputs to their default values.

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
