import os
import time
import subprocess
#loadMockData

TESTING = True
DO_ADD = True



namesToTestDeleteOn = []
emailsToTestDeleteOn = []
with open("C:/test/MOCK_DATA.csv", 'r') as f:
	for i, line in enumerate(f.readlines()):
		#print i
		args = line.replace("\n", "").split(",")
		if i==3 or i==12 or i==14 or i==32 or i==37:
			print "added", args[0], "to namesToTestDeleteOn"
			namesToTestDeleteOn.append(args[0])

		if i==4 or i==13 or i==16:
			print "added", args[1], "to emailsToTestDeleteOn"
			emailsToTestDeleteOn.append(args[1])

		if DO_ADD:
			if i<100:
				if len(line.split(",")) == 4:
					fieldArgs = '-n "{}" -e "{}" -ph "{}" -ad "{}"'.format(args[0],args[1],args[2],args[3])
					cmd = "userDataManager.py -c add -f YAML "+fieldArgs
					if TESTING:
						print "running: ", cmd
					os.system(cmd)

			if i == 101:
				cmd = "userDataManager.py -c convert -f YAML -ctf JSON"
				if TESTING:
					print "running: ", cmd
				os.system(cmd)


			if i>102 and i<203:
				if len(line.split(",")) == 4:
					fieldArgs = '-n "{}" -e "{}" -ph "{}" -ad "{}"'.format(args[0],args[1],args[2],args[3])
					cmd = "userDataManager.py -c add -f JSON "+fieldArgs
					if TESTING:
						print "running: ", cmd
					os.system(cmd)

