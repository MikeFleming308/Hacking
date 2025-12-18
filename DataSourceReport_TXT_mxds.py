#
#---------------------------------------------------------------------------
#
# DataSourceReport_TXT_mxds.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 17/07/2015
# Last updated 31/07/2015
# Description: Opens an *.xls file listing the data source for each layer in the 
# top-most dataframe listed in the mxd Table of Contents.
#
#---------------------------------------------------------------------------

# Import modules
from __future__ import print_function
import os, arcpy, time

# User-supplied parameters
mxdDir = arcpy.GetParameterAsText(0)

# Local variables
dataSourceTXT = mxdDir + "\\MXD_DataSource_Report.txt"
mxds = [m for m in os.listdir(mxdDir) if m.endswith(".mxd")]
setSpace = 50
sp = " "
separator = sp*setSpace
line = "---------------------------------------------------------------------------------------"

# Setup status output
scriptName = 'DataSourceReport_TXT_mxds.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Main
with open(dataSourceTXT, 'w') as outfile:
    for mx in mxds:
        print(mx)
        nextMxd = mxdDir + "\\" + mx
        mxd = arcpy.mapping.MapDocument(nextMxd)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        lyrList = arcpy.mapping.ListLayers(df)
        print("                           ", mx, sep="",end="\n", file=outfile)
        print("LAYER_NAME", "DATA_SOURCE", sep=separator, end="\n", file=outfile)
        print(line, sep="",end="\n", file=outfile)
        for lyr in lyrList:
            if lyr.supports("DATASOURCE"):
	        dSource = os.path.split(lyr.dataSource)[1]
                lname = lyr.name
                space = sp*(setSpace - len(lname))
	        print(lname, dSource, sep=space, end="\n", file=outfile)
        print(line, sep="",end="\n" * 5, file=outfile)

os.startfile(dataSourceTXT)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")




"""





"""










