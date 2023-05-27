import subprocess
import os
import time

os.system('color')


#Variables
applicationFile = ""
applicationName = ""


#Functions
def readConfig():
	import configparser
	global applicationFile, applicationName
	config = configparser.ConfigParser()
	config.read("config.ini")
	applicationFile = config.get("application", "applicationFile")
	applicationName = config.get("application", "applicationName")
	print("\nValues loaded from the config file")
	#print("Application File -->", applicationFile, "\nApplication Name -->", applicationName, "\n[7mClose this window to halt restarting process[0m\n")


def getConfig():
	global applicationFile, applicationName
	print("Application aliver v1.0. Restart any specified application on crash\nPlease [32mrun as adminsitrator[0m. Otherwise it will prompt for admin previlleges each time the target application restart!\n")
	print("Either\n 1) Specify your application path and application name here or\n 2) Specify those in config.ini file\n")
	
	print("Leave application file [1mempty[0m to use values in config file")
	print("Leave application name [1mempty[0m to automatically set the application name")
	print("Type [1m'o'[0m to open GUI file picker\n")
	
	applicationFile = input("Application file - ")
	if (applicationFile == "o") :
		import tkinter as tk
		from tkinter import filedialog
		root = tk.Tk()
		root.withdraw()
		applicationFile = filedialog.askopenfilename()
	if (applicationFile == ""):
		readConfig()
		return

	applicationName = input("Application name - ")
	if (applicationName == ""):
		applicationName = os.path.basename(applicationFile)
		
	if (applicationName == "c"):
		readConfig()
		return

	print("\nApplication specified by user")
		


def process_exists(process_name):
	call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
	# use buildin check_output right away
	output = subprocess.check_output(call).decode()
	# check in last line for process name
	last_line = output.strip().split('\r\n')[-1]
	# because Fail message could be translated
	return last_line.lower().startswith(process_name.lower())


def restartApp():
	restartedTimes = 0
	retries = 0
	try:
		while 1:
			if (not (process_exists(applicationName))):
				print("Application is not running. Restarting...")
				try:
					os.startfile(applicationFile)
				except OSError:
					print("Application failed to start. User may have denied access")
					if retries>=3:
						print("\nApplication continually failed to start for 3 times. Aliver quit")
						print("Application restarted",restartedTimes,"times")
						break
					retries += 1
					time.sleep(3)
					continue
				restartedTimes += 1
				print("Application restarted successfully [{}]".format(restartedTimes))
				print("Application is running")
			#else:
			#    print("Application is running")

			time.sleep(1)
	except KeyboardInterrupt:
		print("\nAliver stopped on keyboard interruption.")
		print("Application restarted",restartedTimes,"times")


#Main sequence
print("[7m Welcome! [0m")
getConfig()
print("Application File -->", applicationFile, "\nApplication Name -->", applicationName, "\n\n[7mAliver started. Close this window or press ctrl+c to halt restarting process[0m\n")
if process_exists(applicationName):
		print("Application is running")
restartApp()
print("[7m Goodbye! [0m")
