"""
Author: Daniel Garnier

This tool was developed as a test, it allows an artist to add users through 
a directory by which they can then search/filter and display in multiple 
formats. 
The tool also has the ability to convert the current data into another file 
format and change locations.
"""
import argparse
import os
import json
import yaml
import re
from functools import partial

DATA_FORMATS = ["JSON", "YAML"]
EXPORT_FORMATS = ["JSON", "YAML", "CSV", "Text"]


class User():
	"""User Object to hold user Attributes
	:param: id, (int), required
	"""
	def __init__(self, id):
		self.id = id

	def setName(self, name):
		"""Sets the Name of the User
		:param: name, (str), required"""
		self.name = name

	def setEmail(self, email):
		"""Sets the email address of the User
		:param: email, (str), required"""
		self.email = email

	def setPhone(self, phone):
		"""Sets the phone number of the User
		:param: phone, (str), required"""
		self.phone = phone

	def setAddress(self, address):
		"""Sets the address of the User
		:param: address, (str), required"""
		self.address = address


class Directory():
	"""Directory Object to hold Users and manage them

	:param: fType, (str), required, the data format type(JSON, YAML)
	:param: dataLocation, (str), required, the location of the data
	"""
	def __init__(self, fType, dataLocation):
		if not hasattr(self, "users"):
			self.users = []
		self.formatType = fType
		self.dataFile = os.path.join(dataLocation, "userData.")


	def getNextId(self):
		""" Gathers the next Id from the currently listed Users
		Returns the new ID"""
		ids = [int(user.id) for user in self.users]
		if len(ids) == 0:
			return 0
		return int(max(ids))+1


	def addUser(self, name, email="", phone="", address=""):
		"""Adds a new user to the Directory
		:param: name, (str), required, name of the new User
		:param: email, (str), optional, email of the new User
		:param: phone, (str), optional, phone number of the new User
		:param: address, (str), optional, address of the new User"""		
		id = str(self.getNextId())
		newUser = User(id)
		newUser.setName(name)
		newUser.setEmail(email)
		newUser.setPhone(phone)
		newUser.setAddress(address)
		self.users.append(newUser)
		print "User Added"


	def findUserIdsByField(self, field, nameFilter):
		"""Filters the Users in the Directory to only those that match the filter
		:param: field, (str), required, the name of the field to filter in, e.g: name, email
		:param: nameFilter (str), required, text to filter the names by, this uses re.search
											to find a match, follow Regular Expression Syntax
		Returns a list of ID's"""
		userIdsFound = []
		for user in self.users:
			matchFound = re.search(nameFilter, eval("user.{}".format(field)))
			if matchFound:
				userIdsFound.append(user.id)
		return userIdsFound


	def findUsersByField(self, field, nameFilter):
		"""Filters the Users in the Directory to only those that match the filter
		:param: field, (str), required, the name of the field to filter in, e.g: name, email
		:param: nameFilter (str), required, text to filter the names by, this uses re.search
											to find a match, follow Regular Expression Syntax
		Returns a list of User Objects"""
		usersFound = []
		for user in self.users:
			matchFound = re.search(nameFilter, eval("user.{}".format(field)))
			if matchFound:
				usersFound.append(user)
		return usersFound


	def displayUsers(self, users, displayFormat, printResult = True):
		"""Prints or returns a list of users based on the format specified
		:param: users, [obj], required, the list of User objects to display
		:param: displayFormat, (str), required, the format to display, this supports:
		                                        JSON, YAML, CSV and Text output
		:param: printResult, (str), optional, defaults to printing the result
		returns the users data based on options given"""
		newUserData = self.convertUsersToDict(users)
		if displayFormat == "JSON":
			res = json.dumps(newUserData)

		elif displayFormat == "YAML":
			res = yaml.dump(
				newUserData, 
				default_flow_style=False, 
				allow_unicode=True
			).replace("!!python/unicode", "")

		elif displayFormat == "CSV":
			res = "Id,Name,Email,Phone,Address,\n"
			for userId in newUserData:
				res+= ",".join([
					userId,
					newUserData[userId]["name"],
					newUserData[userId]["email"],
					newUserData[userId]["phone"],
					newUserData[userId]["address"]
				])+",\n"

		elif displayFormat == "Text":
			res = ""
			for userId in newUserData:
				res += "Id = {id}\tName = {nm}\tEmail = {em}".format(
					id=userId,
					nm=newUserData[userId]["name"],
					em=newUserData[userId]["email"]
				)
				res += "\tPhone Number = {ph}\tAddress = {ad}\n".format(
					ph=newUserData[userId]["phone"],
					ad=newUserData[userId]["address"]
				)

		if printResult:
			print res
		else:
			return res


	def loadUsers(self):
		"""Loads all the users from the Directories data file"""
		userData = readData(self.formatType, self.dataFile)
		for id in userData:
			newUser = User(id)
			newUser.setName(userData[id]["name"])
			newUser.setEmail(userData[id]["email"])
			newUser.setPhone(userData[id]["phone"])
			newUser.setAddress(userData[id]["address"])
			self.users.append(newUser)
		print "Directory Loaded {} Users".format(len(self.users))


	def saveDirectory(self, exportFormat = None, dataLocation = None):
		"""Saves the directory to the specified location and with the given format
		:param: exportFormat, (str), optional, uses the directories current format
											   by default, formats are: JSON and YAML
		:param: dataLocation, (str), optional, uses the directories current location
											   by default"""
		if not exportFormat:
			exportFormat = self.formatType
		if dataLocation:
			dataFile = os.path.join(dataLocation, "userData.")
		else:
			dataFile = self.dataFile
		newUserData = self.convertUsersToDict(self.users)
		writeData(exportFormat, newUserData, dataFile)
		print "Directory Updated"


	def convertUsersToDict(self, users):
		"""Converts a list of User Objects to a Dictionary
		:param: users, (str), required, list of User Objects"""
		newUserData = {}
		for user in users:
			userData = eval(str(user.__dict__))
			del userData["id"]
			newUserData[user.id] = userData
		return newUserData


def runCommand(args):
	""" Base commandline wrapper function"""
	displayFormat = args.displayFormat
	UD = Directory(args.frmt, args.dataLocation)
	UD.loadUsers()
	givenFilters = {
		"name":args.name, 
		"email":args.email, 
		"phone":args.phone, 
		"address":args.address
	}

	filterList = [givenFilters[key] for key in givenFilters]
	if args.cmd == "add":
		UD.addUser(args.name, args.email, args.phone, args.address)
		UD.saveDirectory()

	elif args.cmd == "display":
		if filterList == ["", "", "", ""]:
			users = UD.users
		else:
			users = []
			for fltr in givenFilters:
				if givenFilters[fltr] != "":
					users.extend(UD.findUsersByField(fltr, givenFilters[fltr]))
		UD.displayUsers(users, displayFormat)

	elif args.cmd == "convert":
		UD.saveDirectory(args.convertToFormat, args.dataLocation)


def writeData(dFormat, data, dataFile):
	"""Writes out a data file based on params given
	:param: dFormat, (str), required, Format of the file to write out
	:param: data, (str), required, data to be written to file
	:param: dataFile, (str), required, data file full path and name"""
	if not os.path.exists(os.path.dirname(dataFile)):
		os.makedirs(os.path.dirname(dataFile))
	with open(dataFile+dFormat.lower(), 'w') as f:
		eval("{}.dump({}, {}, indent=4, sort_keys=True)".format(dFormat.lower(), data, f))
	return True


def readData(dFormat, dataFile):
	"""Reads in data from a data file based on params given
	:param: dFormat, (str), required, Format of the file to read from
	:param: dataFile, (str), required, data file full path and name"""
	if not os.path.exists(dataFile+dFormat.lower()):
		data = {}
		return data

	with open(dataFile+dFormat.lower(), 'r') as f:
		data = eval("{}.load({})".format(dFormat.lower(), f))
		return data


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "This tool was developed as a test, it allows an artist to add users through "
		"a directory by which they can then search/filter and display in multiple formats. "
		"The tool also has the ability to convert the current data into another file "
		"format and change locations."
	)

	parser.add_argument(
		"-c",
		"--cmd",
		required=True,
		default = "display",
		choices = ["add","display","convert"],
		help = "The function to run the given args through"
	)

	parser.add_argument(
		"-dl",
		"--dataLocation",
		default = "C:/test/",
		help = "Location of data files"
	)
	parser.add_argument(
		"-f",
		"--frmt",
		required=False,
		default = "JSON",
		choices = DATA_FORMATS,
		help = "Format of the data files to read from/write to"
	)
	parser.add_argument(
		"-ctf",
		"--convertToFormat",
		required=False,
		default = "JSON",
		choices = DATA_FORMATS,
		help = "Format to convert the data files to, requires '-c convert'"
	)

	parser.add_argument(
		"-df",
		"--displayFormat",
		required=False,
		default = "JSON",
		choices = EXPORT_FORMATS,
		help = "The format to display entries as"
	)

	parser.add_argument(
		"-n",
		"--name",
		default = "",
		help = "The name of the entry to add, or the filter to search by"
	)

	parser.add_argument(
		"-ad",
		"--address",
		default = "",
		help = "The address of the entry to add, or the filter to search by"
	)

	parser.add_argument(
		"-ph",
		"--phone",
		default = "",
		help = "The phone of the entry to add, or the filter to search by"
	)

	parser.add_argument(
		"-e",
		"--email",
		default = "",
		help = "The email of the entry to add, or the filter to search by"
	)

	args = parser.parse_args()
	runCommand(args)
