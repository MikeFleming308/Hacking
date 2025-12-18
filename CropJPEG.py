#
#---------------------------------------------------------------------------
#
# CropJPEG.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 12/05/2017
# Last updated 12/05/2017
# Description: 
#
#---------------------------------------------------------------------------

# Import modules
import os, arcpy, time
from PIL import Image

# User-supplied parameters
jpegDir = arcpy.GetParameterAsText(0) # Get path to jpeg directory
top = float(arcpy.GetParameterAsText(1))# Get map element extents for cropping
left = float(arcpy.GetParameterAsText(2))
right = float(arcpy.GetParameterAsText(3))
bottom = float(arcpy.GetParameterAsText(4))
box = (left, top, right, bottom)

# Local variables
counter = 0

# Setup status output
scriptName = 'CropJPEG.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
os.chdir(jpegDir)
jpgs = os.listdir(jpegDir)
jpgs.sort()
total = len(jpgs)
msg = "\n{} *.jpg files found. \n".format(total)
arcpy.AddMessage(msg)

# Main
for j in jpgs:
    counter += 1
    fnum = str(counter)
    if len(fnum) < 2:
        fnum = "0{}".format(fnum)
    if j.endswith(".jpg"):
        jpg = Image.open(j)
        region = jpg.crop(box)
        fname = "Sheet_{}.jpg".format(fnum)
        region.save(fname, "JPEG")
        arcpy.AddMessage(fname)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")
