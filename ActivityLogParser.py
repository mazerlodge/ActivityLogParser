#!/usr/local/bin/python3

# vars
fn = "./data/SampleActivityLog.txt"
tagDict = {}

# Read the activity log
file = open(fn, "r")
lines = file.readlines()
file.close()

# group lines from the log according to the line tag. 
# Note: line tag = start of line text between dash and comma.
for aLine in lines: 
	if (aLine[0] == '\t'):
		commaPos = aLine.find(',')
		if (commaPos > -1):
			categoryTag = aLine[3:commaPos]
			outLine = '- ' + aLine[commaPos+2:].rstrip()
			#print("%s --> %s" % (categoryTag, outLine.rstrip())) 

			# is current categoryTag in the dictionary already
			categoryList  = tagDict.get(categoryTag)
			if categoryList == None: 
				print("New category")
				categoryList = []
				categoryList.append(outLine)  
				tagDict[categoryTag] = categoryList 
			else: 
				categoryList.append(outLine)
				print("Added, list now %d to category [%s]" % (len(categoryList), outLine))

# Output lines grouped by tags
for aKey in tagDict: 
	print(aKey) 
	aList = tagDict[aKey]
	for aLine in aList:
		print("\t%s" % aLine) 
