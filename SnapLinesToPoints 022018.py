#---------------------------------------------------------------------------
# Created: 15/06/2017
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Last updated 15/02/2018 - Adelmo Cos
# Description: Takes 2 layers as input, 1 x point and 1 x line. 
#              Finds closest point to line node, extends line to node without
#              altering existing line geometry. 
#              Third input parameter is maximum distance to search and extend lines
#              Not designed for multipart lines.
#---------------------------------------------------------------------------

# Import modules
import os, arcpy, time
arcpy.env.workspace = "C:\Users\41252\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\QA.sde"

# Start an edit session. Must provide the workspace.
edit = arcpy.da.Editor("Database Connections\\QA.sde")

# Edit session is started without an undo/redo stack for versioned data
#  (for second argument, use False for unversioned data)
edit.startEditing(False, True)

# Start an edit operation
edit.startOperation()

# User-supplied parameters
lines = arcpy.GetParameterAsText(0)
points = arcpy.GetParameterAsText(1)
distance = arcpy.GetParameterAsText(2)
dist = str(distance) + " meters"

# Local variables
linedict = {}
pointdict = {}
search_fields = ["OID@", "SHAPE@"]
change_dict = {}

# Setup status output
scriptName = 'SnapLinesToPoints_EditorLicence.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Setup 

with arcpy.da.SearchCursor(lines, search_fields) as cur:
    for row in cur:
        linedict[row[0]] = (row[1].firstPoint, row[1].lastPoint)

with arcpy.da.SearchCursor(points, search_fields) as cur:
    for row in cur:
        pointdict[row[0]] = row[1]
        
for lne in linedict:
    start_node = []
    end_node = []
    for pnt in pointdict:
        sndist = pointdict[pnt].distanceTo(linedict[lne][0])
        endist = pointdict[pnt].distanceTo(linedict[lne][1])
        start_node.append([sndist, pnt])
        end_node.append([endist, pnt])
        start_node.sort()
        end_node.sort()
        sdist = start_node[0][0]
        edist = end_node[0][0]
        if sdist <= float(distance):
            startpnt = start_node[0][1]
        else:
            startpnt = None
        if edist <= float(distance):
            endpnt = end_node[0][1]
        else:
            endpnt = None
        if startpnt is None and endpnt is None:
            pass
        else:
            change_dict[lne] = (startpnt, endpnt)
        
# Main
with arcpy.da.UpdateCursor(lines, ["OID@", "SHAPE@"]) as cur:
    for row in cur:
        if row[0] in change_dict:
            array = arcpy.Array()
            for i in row[1]:
                for j in i:
                    array.add(j)
            if change_dict[row[0]][0] is not None:
                array[0] = pointdict[change_dict[row[0]][0]].firstPoint
            if change_dict[row[0]][1] is not None:
                array[-1] = pointdict[change_dict[row[0]][1]].firstPoint
            row[1] = arcpy.Polyline(array)
        cur.updateRow(row)
# Stop the edit operation.
edit.stopOperation()

# Stop the edit session and save the changes
#edit.stopEditing(False) 

arcpy.RefreshActiveView()

# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")



