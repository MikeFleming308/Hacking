#
#---------------------------------------------------------------------------
#
# DataSourceReport_XLS.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 17/07/2015
# Last updated 27/07/2015
# Description: Opens an *.xls file listing the data source for each layer in the 
# top-most dataframe listed in the mxd Table of Contents.
#
#---------------------------------------------------------------------------

# Import modules
# from __future__ import print_function
import os, arcpy, time, xlwt

# User-supplied parameters


# Local variables
header = ["TOC_NO", "LAYER_NAME", "FEATURE_CLASS", "DATA_SOURCE"]
rowNo = 0



# Setup status output
scriptName = 'DataSourceReport_XLS.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup 
mxd = arcpy.mapping.MapDocument("CURRENT")
mxdPath = str(mxd.filePath)
splitPath = os.path.split(mxdPath)
dataSourceXLS = splitPath[0] + "\\" + splitPath[1][:-4] + "_MXD_DataSource_Report.xls"
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyrList = arcpy.mapping.ListLayers(df)
book = xlwt.Workbook()
sheet = book.add_sheet("Data Sources")


# Main
sheet.write(0, 0, header[0])
sheet.write(0, 1, header[1])
sheet.write(0, 2, header[2])
sheet.write(0, 3, header[3])

for lyr in lyrList:
    if lyr.supports("DATASOURCE"):
        dSource = os.path.split(lyr.dataSource)
        rowNo += 1
        sheet.write(rowNo, 0, rowNo)
        sheet.write(rowNo, 1, lyr.name)
        sheet.write(rowNo, 2, dSource[1])
        sheet.write(rowNo, 3, dSource[0])
book.save(dataSourceXLS)
os.startfile(dataSourceXLS)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")
