#
#---------------------------------------------------------------------------
#
# MoveUsingOtherFeatureGeometry.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 19/06/2016
# Last updated 19/06/2016
# Description: Replaces the geometry in a feature class (The "From" feature calls) with the geometry of a second feature class (The "To" feature class).
# Requires 2 feature classes of the same geometry type with a common field with unique values. For example, where a value in the TREE_ID field in the "To" fc 
# matches with a value in the TREE_ID field in the "From" fc, the geometry will be overwritten in the "From" fc.
#---------------------------------------------------------------------------

# Import modules
import os, arcpy, time


# User-supplied parameters
fromFC = arcpy.GetParameterAsText(0)
toFC = arcpy.GetParameterAsText(1)
fromField = arcpy.GetParameterAsText(2)
toField = arcpy.GetParameterAsText(3)

# Local variables
geoDict = {}
counter = 0

# Environmental settings
arcpy.env.workspace = os.path.split(fromFC)[0]
ws = arcpy.env.workspace

# Setup status output
scriptName = 'MoveUsingOtherFeatureGeometry.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)


# Setup

msg = "Creating a search cursor in the feature class '{}' to populate a dictionary with the values from the {} field as the key and the geometry object as the value".format(toFC, toField)
arcpy.AddMessage(msg)
with arcpy.da.SearchCursor(toFC, [toField, "SHAPE@"]) as cur: # Get common value and geometry object from the "To" feature class
    for row in cur:
        geoDict[row[0]] = row[1] # Add common value as key and geometry object as value to dictionary
msg = "Dictionary created with {} values.".format(len(geoDict))
arcpy.AddMessage(msg)


# Main
msg = "Starting the geometry update process... "
arcpy.AddMessage(msg)
msg = "Opening edit session... "
arcpy.AddMessage(msg)

try:

    with arcpy.da.Editor(ws) as edit: 

        with arcpy.da.UpdateCursor(fromFC, [fromField, "SHAPE@"]) as cur: # Iterate through rows
            for row in cur:
                if row[0] in geoDict: # Check if there is a matching value
                    counter += 1
                    row[1] = geoDict[row[0]] # Overwrite existing geometry with geometry from dictionary
                    if counter % 10 == 0:
                        # arcpy.RefreshActiveView()
                        msg = str(counter) + " trees moved"
                        # msg = "Geometry updated for {} {}".format(fromField, row[0])
                        arcpy.AddMessage(msg)
                    cur.updateRow(row)
                    arcpy.RefreshActiveView()
except arcpy.ExecuteError:
    msg = arcpy.GetMessages(2)
    arcpy.AddMessage(msg)

arcpy.RefreshActiveView()
msg = "Total of " + str(counter) + " trees moved"
arcpy.AddMessage(msg)
# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

