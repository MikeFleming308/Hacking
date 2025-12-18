#
#---------------------------------------------------------------------------
#
# DataSourceReport_XLS_Multi_SingleTable.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 17/07/2015
# Last updated 31/07/2015
# Description: Opens an *.xls workbook listing the data source for each mxd.
#  
# NOTE: Only show layers from the top-most dataframe listed in the mxd Table of Contents.
#
#---------------------------------------------------------------------------

# Import modules
# from __future__ import print_function
import os, arcpy, time, xlwt

# User-supplied parameters
mxdDir = arcpy.GetParameterAsText(0)

# Local variables
mxds = [m for m in os.listdir(mxdDir) if m.endswith(".mxd")]
header = ["MXD", "TOC_NO", "LAYER_NAME", "FEATURE_CLASS", "DATA_SOURCE"]
dataSourceXLS = mxdDir + "\\Multiple_MXD_DataSource_ReportTable.xls"
book = xlwt.Workbook()
rowNo = 0


# Setup status output
scriptName = 'DataSourceReport_XLS_Multi_SingleTable.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Main

sheet = book.add_sheet('DataSourceReport')
sheet.write(0, 0, header[0])
sheet.write(0, 1, header[1])
sheet.write(0, 2, header[2])
sheet.write(0, 3, header[3])
sheet.write(0, 4, header[4])


for mx in mxds:
    msg = "Now reading {}\n".format(mx)
    arcpy.AddMessage(msg)
    tocNo = 0
    nextMxd = mxdDir + "\\" + mx
    mxd = arcpy.mapping.MapDocument(nextMxd)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    lyrList = arcpy.mapping.ListLayers(df)
    for lyr in lyrList:
        rowNo += 1
        tocNo += 1
        if lyr.supports("DATASOURCE"):
            dSource = os.path.split(lyr.dataSource)
            sheet.write(rowNo, 0, mx[:-4])
            sheet.write(rowNo, 1, tocNo)
            sheet.write(rowNo, 2, lyr.name)
            sheet.write(rowNo, 3, dSource[1])
            sheet.write(rowNo, 4, dSource[0])
        elif lyr.isGroupLayer:
            sheet.write(rowNo, 0, mx[:-4])
            sheet.write(rowNo, 1, tocNo)
            sheet.write(rowNo, 2, lyr.name)
            sheet.write(rowNo, 3, "Group Layer")

book.save(dataSourceXLS)
os.startfile(dataSourceXLS)

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")
