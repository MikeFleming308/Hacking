#
#---------------------------------------------------------------------------
#
# Profoma.py
# Mike Fleming mcfleming@goldcoast.qld.gov.au
# Created: 01/10/2017
# Last updated 01/10/2017
# Description: 
#
#---------------------------------------------------------------------------

# Import modules
import arcpy, time, csv
from os import walk

# User-supplied parameters
#Read input parameters from script tool
# csv_folder = arcpy.GetParameterAsText(0)
# output_folder = arcpy.GetParameterAsText(1)
# fieldNo_org = arcpy.GetParameterAsText(2)
# fieldNo_org_addr = arcpy.GetParameterAsText(3)
# fieldNo_org_lat = arcpy.GetParameterAsText(4)
# fieldNo_org_lon = arcpy.GetParameterAsText(5)
# fieldNo_emp_lat = arcpy.GetParameterAsText(6)
# fieldNo_emp_lon = arcpy.GetParameterAsText(7)
# fieldNo_cmode = arcpy.GetParameterAsText(8)
# fieldNo_fmode = arcpy.GetParameterAsText(9)

csv_folder = r"E:\Users\Mike\Documents\Coding"
output_folder = r"E:\Users\Mike\Documents\Coding\out"
fieldNo_org = 0
fieldNo_org_addr = 3
fieldNo_org_lat = 1
fieldNo_org_lon = 2
fieldNo_emp_lat = 4
fieldNo_emp_lon = 5
fieldNo_cmode = 6
fieldNo_fmode = 7

# Local variables
header = ["ORG", "ORG_SITE_LAT", "ORG_SITE_LON", "ORG_SITE_ADDRESS", "EMP_LAT",	"EMP_LON", "C_MODE", "F_MODE"]
env.workspace = csv_folder


f = []

csvs =[]
# for file in os.listdir(cod):
# if file.endswith(".csv"):
    # csvs.append(file)

  #  datarows[0][3:]
    
datarows =[]

csvs = [file for file in arcpy.ListFiles("*.csv")]
for cs in csvs:
    with open(cs, 'rb') as csvfile:
        orgrows = []
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            orgrows.append(row)
        datarows.append(orgrows)

     for cs in csvs:
    ...:     ...:     with open(cs, 'rb') as csvfile:
    ...:     ...:         csvreader = csv.reader(csvfile)
    ...:     ...:         for row in csvreader:
    ...:     ...:             datarows.append(row)   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# Setup status output
scriptName = 'Profoma.py'
StartTime = time.strftime("%#c", time.localtime())
startText = "____________________Script started successfully.____________________"
arcpy.AddMessage(" " * 3)
arcpy.AddMessage("         -<>-<>-<>-" * 3)
arcpy.AddMessage(" ")
arcpy.AddMessage(startText)
arcpy.AddMessage("\n")
arcpy.AddMessage(StartTime)

# Main



# Final status output
arcpy.AddMessage("\nStarted  " + scriptName)
arcpy.AddMessage(StartTime)
arcpy.AddMessage("\nFinished " + scriptName)
finishTime = time.strftime("%#c", time.localtime())
arcpy.AddMessage(finishTime)
arcpy.AddMessage("\n=====================================================================")

