# mineman-1.0
# ===============================================
# This program is released under public domain
# all code within this program may be used
# anywhere, freely.
# ===============================================
#!/usr/bin/python

import os
import sys
from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import shutil
import ConfigParser


osName="Windows"
homedir=os.path.expanduser("~")
print homedir
datadir=homedir+"\\AppData\\Roaming\\mineman"
print datadir

class M (object):
	def __init__(self):
		pass

	def empty(self):
		print "Unimplimented option."
		pass

	def addLauncher(self):
		launchertoadd=""
		launchertoadd = askopenfilename()
		print launchertoadd

	def exitProg(self):
		print "Exiting program...."
		sys.exit()

	def rmDataDir(self):
		print "Removing data directory..."
		#os.remove(datadir)
		shutil.rmtree(datadir)
		print "Directory removed."

	def makeDataDir(self):
		print "Creating a new data directory..."
		os.makedirs(datadir)
		os.makedirs(datadir+"\\launchers")
		os.makedirs(datadir+"\\dataslots")
		os.makedirs(datadir+"\\dataslots\slot1")
		os.makedirs(datadir+"\\dataslots\slot2")
		os.makedirs(datadir+"\\dataslots\slot3")
		os.makedirs(datadir+"\\dataslots\slot4")
		os.makedirs(datadir+"\\dataslots\slot5")
		shutil.copyfile("default.conf", datadir+"\\main.conf")
		print "Created sucessfuly.\n"

	def startupChecks(self):
		if osName == "Windows":
			if not os.path.exists(datadir):
				print "Data directory not found."
				self.makeDataDir()
			else:
				pass
		else:
			print "Error. No data directory could be found due to unknown OS. Data directory being written in program folder."
		mainCfg=ConfigParser.SafeConfigParser()
		mainCfg.read(datadir+"\\main.conf")

		if mainCfg.get("startup", "debug")=="yes":
			debug1=1
		else:
			debug1=0





m=M()

def exit2():
	sys.exit()

def mainprog():
	print "Starting MineMan 1.0....."
	print ""
	m.startupChecks()
	print ""
	print "Currently this program is a work in progress. \nSome features may not be implimented yet."
	mainwin=Tk()
	mainwin.title("MineMan 1.0")
	mainwin.geometry("500x300")


# Menu Funcitons ======================================
	menubar=Menu(mainwin)

	filemenu=Menu(menubar, tearoff=0)
	filemenu.add_command(label="Add a Launcher", command=m.addLauncher)
	filemenu.add_command(label="Save Config", command=m.empty)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=m.exitProg)
	menubar.add_cascade(label="File", menu=filemenu)

	backupmenu=Menu(menubar, tearoff=0)
	backupmenu.add_command(label="Backup One Slot", command=m.empty)
	backupmenu.add_command(label="Backup All Slots to Zip File", command=m.empty)
	backupmenu.add_command(label="Save Launcher From List", command=m.empty)
	menubar.add_cascade(label="Backup", menu=backupmenu)

	optionsmenu=Menu(menubar, tearoff=0)
	optionsmenu.add_command(label="Edit Launchers", command=m.empty)
	optionsmenu.add_command(label="Edit Data Slots", command=m.empty)
	optionsmenu.add_command(label="Delete Data", command=m.rmDataDir)
	menubar.add_cascade(label="Options", menu=optionsmenu)

	helpmenu=Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About", command=m.empty)
	menubar.add_cascade(label="Help", menu=helpmenu)

# =====================================================

	controlFrame = Frame(mainwin)
	startLauncherBtn1 = Button(controlFrame, text="Start the Launcher")
	exitMineManBtn1 = Button(controlFrame, text="Exit", command = m.exitProg)

	launcherFrame= Frame(mainwin)
	launcherLabel = Label(launcherFrame, text="Launchers available:")

	dataFrame = Frame(mainwin)
	dataLabel= Label(dataFrame, text="Data folders available: ")

	controlFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
	startLauncherBtn1.pack(side=RIGHT, padx=5)
	exitMineManBtn1.pack(side =RIGHT, padx=5)

	launcherFrame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
	launcherLabel.pack(side=LEFT, pady=5)

	dataFrame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
	dataLabel.pack(side=LEFT, pady=5)

	mainwin.config(menu=menubar)
	mainwin.mainloop()

mainprog()