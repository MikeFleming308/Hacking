#
#---------------------------------------------------------------------------
#
# GetRowCount.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 13/11/2015
# Last updated 13/11/2015
# Description: Produces a text file listing the number of rows for each feature class in the 
#              current mxd. 
#              Warns if a definition query may be limiting the number of records returned.
#
#---------------------------------------------------------------------------

# Import modules
from __future__ import print_function
import os, arcpy, time


# Local variables
fName = "RowCount.txt"


# Setup status output
scriptName = 'GetRowCount.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup
mxd = arcpy.mapping.MapDocument("CURRENT") # create MapDocument object
df = mxd.activeDataFrame                   # create DataFrame object 
lyrList = arcpy.mapping.ListLayers(mxd, "", df)  # create list of layers
splitPath = os.path.split(mxd.filePath)
filePath = splitPath[0] + "\\" + fName

# Main
with open(filePath, 'w') as outFile:
    for lyr in lyrList:
        if lyr.supports("DATASOURCE"):
            desc = arcpy.Describe(lyr)
            wc = desc.whereClause
            arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
            recs = str(arcpy.GetCount_management(lyr))
            print('\n', sep=' ', end='\n', file=outFile)
            calc = 50 - len(lyr.name)
            space = str(" "*calc)
            print(lyr.name, recs, sep=space, end='\n', file=outFile)
            print('--------------------------------',  sep=' ', end='\n', file=outFile)

            if wc != "":
                print("Note! This layer has a definition query!", sep=' ', end='\n', file=outFile)
                print(wc, sep=' ', end='\n', file=outFile)


os.startfile(filePath)


# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

