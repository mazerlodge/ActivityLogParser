#!/usr/local/bin/python3

import sys 
from ArgTools import ArgParser

def debugMsg(msg): 
	global bInDebug

	if (bInDebug):
		print(msg) 

def getCodePath():
	launchFile = sys.argv[0]
	launchFileReversed = launchFile[::-1]
	if launchFileReversed.find('/') == -1:
		lastSlashPos = 0
		pathPart = "."
	else: 
		lastSlashPos = launchFileReversed.index('/')
		pathPart = launchFile[0:len(launchFile)-lastSlashPos]

	return(pathPart)
 

# vars
codePath = getCodePath()
inFilename = codePath + "/data/in.txt"
outFilename = "NOT_SET"
bInDebug = False
tagDict = {}
ap = ArgParser(sys.argv)

# check command line for input and/or output filename(s) 
if (ap.isInArgs("-in", True)):
	inFilename = ap.getArgValue("-in")

if (ap.isInArgs("-out", True)):
	outFilename = ap.getArgValue("-out")

# check command line for debug mode
if (ap.isInArgs("-debug", False)): 
	bInDebug = True

# Read the activity log
inFile = open(inFilename, "r")
lines = inFile.readlines()
inFile.close()

# group lines from the log according to the line tag. 
# Note: line tag = start of line text between dash and comma.
for aLine in lines: 
	if (aLine[0] == '\t'):
		commaPos = aLine.find(',')
		if (commaPos > -1):
			categoryTag = aLine[3:commaPos]
			outLine = '- ' + aLine[commaPos+2:].rstrip()

			# is current categoryTag in the dictionary already
			categoryList  = tagDict.get(categoryTag)
			if categoryList == None: 
				debugMsg("New category [%s]" % categoryTag)
				categoryList = []
				categoryList.append(outLine)  
				tagDict[categoryTag] = categoryList 
			else: 
				categoryList.append(outLine)
				debugMsg("Added, list now %d long, entry is [%s]" % (len(categoryList), outLine))

# Output lines grouped by tags
print("")
for aKey in tagDict: 
	print(aKey) 
	aList = tagDict[aKey]
	for aLine in aList:
		print("\t%s" % aLine) 
	print("")

# Prepare the output file if one was specified 
if (outFilename != "NOT_SET"): 
	outFile = open(outFilename, "w")
	for aKey in tagDict: 
		outLine = "%s\n" % aKey
		outFile.write(outLine)
		aList = tagDict[aKey]
		for aLine in aList:
			outLine = "\t%s\n" % aLine
			outFile.write(outLine)
		outFile.write("\n")

	outFile.flush() 
	outFile.close()
	
