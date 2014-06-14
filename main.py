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

class M (object):
	def __init__(self):
		pass

	def addLauncher(self):
		pass

	def exitProg(self):
		print "Exiting program...."
		sys.exit()

m=M()

def exit2():
	sys.exit()

def mainprog():
	print "Starting MineMan 1.0....."
	print ""
	print "Currently this program is a work in progress. Some features may not be implimented yet."
	mainwin=Tk()
	mainwin.title("MineMan 1.0")
	mainwin.geometry("500x300")

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


	mainwin.mainloop()

mainprog()