#
#---------------------------------------------------------------------------
#
# SnapLinesToPoints.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 15/06/2017
# Last updated 14/02/2018
# Description: Takes 2 layers as input, 1 x point and 1 x line. 
#              Finds closest point to line node, extends line to node without
#              altering existing line geometry. 
#              Third input parameter is maximum distance to search and extend lines
#              Not designed for multipart lines.
#---------------------------------------------------------------------------

# Import modules
import os, arcpy, time, getpass

arcpy.env.workspace="Database Connections\PG3.sde"
userID=getpass.getuser()

# User-supplied parameters
lines = arcpy.GetParameterAsText(0)
points = arcpy.GetParameterAsText(1)
distance = arcpy.GetParameterAsText(2)


# Local variables
dist = str(distance) + " meters"
start = "in_memory\start"
end = "in_memory\end"
StartDict = {}
EndDict = {}
fieldList = ["ORIG_FID", "NEAR_FID", "NEAR_X", "NEAR_Y"] 
arcpy.FeatureVerticesToPoints_management(lines, start,"START")
arcpy.FeatureVerticesToPoints_management(lines, end, "END")
arcpy.Near_analysis(start, points, dist, "LOCATION", "NO_ANGLE")
arcpy.Near_analysis(end, points, dist, "LOCATION", "NO_ANGLE")


# Setup status output
scriptName = 'SnapLinesToPoints.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Setup 
with arcpy.da.SearchCursor(start, fieldList) as cur: 
    for row in cur:
        if row[1] > 0:
            StartDict[row[0]] = (row[2], row[3])
del start
arcpy.Delete_management("in_memory\start")

with arcpy.da.SearchCursor(end, fieldList) as cur:
    for row in cur:
        if row[1] > 0:
            EndDict[row[0]] = (row[2], row[3])
del end
arcpy.Delete_management("in_memory\end")

# Main
# Start an edit session. Must provide the workspace.
edit = arcpy.da.Editor(arcpy.env.workspace)

# Edit session is started without an undo/redo stack for versioned data
#  (for second argument, use False for unversioned data)
edit.startEditing(False, True)

# Start an edit operation
 edit.startOperation()

with arcpy.da.UpdateCursor(lines, ["OID@", "SHAPE@"]) as cur:
    for row in cur:
        if row[0] in StartDict or row[0] in EndDict:
            array = arcpy.Array()
            for i in row[1]:
                for j in i:
                    array.add(j)
            if row[0] in StartDict:
                array[0] = arcpy.Point(StartDict[row[0]][0], StartDict[row[0]][1])
            if row[0] in EndDict:
                array[-1] = arcpy.Point(EndDict[row[0]][0], EndDict[row[0]][1])
            row[1] = arcpy.Polyline(array)
        cur.updateRow(row)

# Stop the edit operation.
edit.stopOperation()

 # Stop the edit session and save the changes
edit.stopEditing(True)        
        
# arcpy.RefreshActiveView()

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

