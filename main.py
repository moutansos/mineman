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
datadir=homedir+"\\AppData\\Roaming\\mineman"
mainCfg=ConfigParser.SafeConfigParser()
mainCfg.read(datadir+"\\main.conf")

class M (object):
	def __init__(self):
		pass

	def empty(self):
		print "Unimplimented option."
		pass

	## BACKEND FUNCTIONS ====================================


	def addLauncherSlotSpec1(self):
		self.addLauncherSlotSpec("1")
	def addLauncherSlotSpec2(self):
		self.addLauncherSlotSpec("2")
	def addLauncherSlotSpec3(self):
		self.addLauncherSlotSpec("3")
	def addLauncherSlotSpec4(self):
		self.addLauncherSlotSpec("4")
	def addLauncherSlotSpec5(self):
		self.addLauncherSlotSpec("5")


	def addDataSlotSpec1(self):
		self.addDataSlotSpec("1")
	def addDataSlotSpec2(self):
		self.addDataSlotSpec("2")
	def addDataSlotSpec3(self):
		self.addDataSlotSpec("3")
	def addDataSlotSpec4(self):
		self.addDataSlotSpec("4")
	def addDataSlotSpec5(self):
		self.addDataSlotSpec("5")



	def startlauncher(self):
		print "Starting launcher..."
		launcherslot=""
		try:
			launcherslot=str(LaunVar.get())
		except:
			print "ERROR: No launcher specified."
		print launcherslot



	## ----- SLOT SPECIFIC FUNCITONS.
	def addLauncherSlotSpec(self, launchnum):
		print "Adding launcher to Slot "+launchnum
		launtoadd=askopenfilename()
		if launtoadd=="":
			print "ERROR: No file specified. Aborting launcher add."
		else:
			print "Launcher file specified: "+launtoadd
			LaunName=""
			def getNameFromDiag():
				LaunName=GNDmainEntry.get()
				

				print "Launcher Name: "+LaunName
				if LaunName=="":
					print "ERROR: No name was specified"
				else:
					getNameDiag.destroy()
					lauchnumLong="slot"+launchnum

					print "Copying launcher to launcher directory."
					shutil.copyfile(launtoadd, datadir+"\\launchers\\slot"+launchnum+".jar")

					mainCfg.set("launchers", lauchnumLong, datadir+"\\launchers\\slot"+launchnum+".jar")
					mainCfg.set("launchers", lauchnumLong+"Name", LaunName)
					print "Saving changes to config file."
					with open(datadir+"\\main.conf", 'wb') as configfile:
						mainCfg.write(configfile)

			getNameDiag=Tk()
			getNameDiag.title("Input Launcher Name")
			GNDmainLabel=Label(getNameDiag, text="Please input a launcher name: ")
			GNDmainEntry=Entry(getNameDiag, text="")
			GNDmainButton=Button(getNameDiag, text="Ok", command=getNameFromDiag)
			GNDmainLabel.pack(padx=20, pady=10)
			GNDmainEntry.pack(padx=20, pady=10, fill=X)
			GNDmainButton.pack(padx=20, pady=10)
			getNameDiag.mainloop()

	def addDataSlotSpec(self, datanum):
		## This is the add data function that is not working. Under construction.
		print "Adding a new data slot."
		def getSlotFromDiag():
			DataName=ADSmainEntry.get()
			if DataName=="":
				print "ERROR: No name was specified."
			else:
				addDataWin.destroy()
				slotNumber="slot"+datanum+"Name"

				def newDataSlot():
					ANOOmainWin.destroy()
					os.mkdir(datadir+"\\dataslots\\slot"+datanum+"\\.minecraft")
					mainCfg.set("data", slotNumber, DataName)
					print "Saving changes to config file."
					with open(datadir+"\\main.conf", 'wb') as configfile:
						mainCfg.write(configfile)

				def oldDataSlot():
					ANOOmainWin.destroy()
					datatoget=askdirectory()
					try:
						shutil.rmtree(datadir+"\\dataslots\\slot"+datanum+"\\.minecraft")
					except:
						pass
					shutil.copytree(datatoget, datadir+"\\dataslots\\slot"+datanum+"\\.minecraft")
					mainCfg.set("data", slotNumber, DataName)
					print "Saving changes to config file."
					with open(datadir+"\\main.conf", 'wb') as configfile:
						mainCfg.write(configfile)

				ANOOmainWin=Tk()
				ANOOmainWin.title("New slot or choose data file?")
				ANOOmainLabel=Label(ANOOmainWin, text="Is this a new slot or do you have an old minecraft directory for this slot?")
				ANOOnewBtn=Button(ANOOmainWin, text="New", command=newDataSlot)
				ANOOoldBtn=Button(ANOOmainWin, text="Old", command=oldDataSlot)
				ANOOmainLabel.pack(padx=20, pady=10)
				ANOOnewBtn.pack(padx=20, pady=10)
				ANOOoldBtn.pack(padx=20, pady=10)
				ANOOmainWin.mainloop


		addDataWin=Tk()
		addDataWin.title("Specify a name for this slot.")
		ADSmainLabel=Label(addDataWin, text="Please specify a name for this data slot: ")
		ADSmainEntry=Entry(addDataWin)
		ADSmainButton=Button(addDataWin, text="Ok", command=getSlotFromDiag)
		ADSmainLabel.pack(padx=20, pady=10)
		ADSmainEntry.pack(padx=20, pady=10, fill=X)
		ADSmainButton.pack(padx=20, pady=10)
		addDataWin.mainloop()
		





	## END SLOT SPECIFIC FUNCTIONS.

	def backupSingleSlot(self):
		print "Backup single slot started."


	def exitProg(self):
		print "Exiting program...."
		mainwin.destroy()

	def rmDataDir(self):
		print "Removing data directory..."
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

	#STARTUP FUNCTIONS ==========================================================

	def startupChecks(self):
		if osName == "Windows":
			if not os.path.exists(datadir):
				print "Data directory not found."
				self.makeDataDir()
			else:
				pass
		else:
			print "Error. No data directory could be found due to unknown OS. Data directory being written in program folder."


		print mainCfg.get("startup", "version")
		if mainCfg.get("startup", "debug")=="yes":
			debug1=1
		else:
			debug1=0

		try:
			print "\n Loading launchers from config..."
			launcher1=mainCfg.get("launchers", "slot1")
			launcher1Name=mainCfg.get("launchers", "slot1Name")
			print "Launcher1 Loaded"
			launcher2=mainCfg.get("launchers", "slot2")
			launcher2Name=mainCfg.get("launchers", "slot2Name")
			print "Launcher2 Loaded"
			launcher3=mainCfg.get("launchers", "slot3")
			launcher3Name=mainCfg.get("launchers", "slot3Name")
			print "Launcher3 Loaded"
			launcher4=mainCfg.get("launchers", "slot4")
			launcher4Name=mainCfg.get("launchers", "slot4Name")
			print "Launcher4 Loaded"
			launcher5=mainCfg.get("launchers", "slot5")
			launcer5Name=mainCfg.get("launchers", "slot5Name")
			print "Launcher5 Loaded"
			print " All launchers loaded sucessfuly.\n\n Proceeding to load data slots."

			data1=mainCfg.get("data", "slot1Name")
			print "Dataslot1 Loaded."
			data2=mainCfg.get("data", "slot2Name")
			print "Dataslot2 Loaded."
			data3=mainCfg.get("data", "slot3Name")
			print "Dataslot3 Loaded."
			data4=mainCfg.get("data", "slot4Name")
			print "DataSlot4 Loaded."
			data5=mainCfg.get("data", "slot5Name")
			print "Dataslot5 Loaded.\n All dataslots sucessfuly loaded.\n\n"
		except:
			print "One or more config values was not found. Program will probably crash. Delete datafolder and start over."



m=M()

def exit2():
	sys.exit()

def mainprog():
	print "Starting MineMan 1.0....."
	print ""
	m.startupChecks()
	print ""
	print "Currently this program is a work in progress. \nSome features may not be implimented yet.\n\n"
	mainwin=Tk()
	mainwin.title("MineMan 1.0")
	mainwin.geometry("500x350")


# Menu Funcitons ======================================
	menubar=Menu(mainwin)

	filemenu=Menu(menubar, tearoff=0)
	filemenu.add_command(label="Add a Launcher", command=m.empty)
	filemenu.add_command(label="Save Config", command=m.empty)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=mainwin.destroy)
	menubar.add_cascade(label="File", menu=filemenu)

	# Launcher menu++++++++++++
	launchermenu=Menu(menubar, tearoff=0)

	launcherslot1cascade=Menu(launchermenu, tearoff=0)
	launcherslot1cascade.add_command(label="Add Launcher", command=m.addLauncherSlotSpec1)
	launchermenu.add_cascade(label="Slot 1", menu=launcherslot1cascade)

	launcherslot2cascade=Menu(launchermenu, tearoff=0)
	launcherslot2cascade.add_command(label="Add Launcher", command=m.addLauncherSlotSpec2)
	launchermenu.add_cascade(label="Slot 2", menu=launcherslot2cascade)

	launcherslot3cascade=Menu(launchermenu, tearoff=0)
	launcherslot3cascade.add_command(label="Add Launcher", command=m.addLauncherSlotSpec3)
	launchermenu.add_cascade(label="Slot 3", menu=launcherslot3cascade)

	launcherslot4cascade=Menu(launchermenu, tearoff=0)
	launcherslot4cascade.add_command(label="Add Launcher", command=m.addLauncherSlotSpec4)
	launchermenu.add_cascade(label="Slot 4", menu=launcherslot4cascade)

	launcherslot5cascade=Menu(launchermenu, tearoff=0)
	launcherslot5cascade.add_command(label="Add Launcher", command=m.addLauncherSlotSpec5)
	launchermenu.add_cascade(label="Slot 5", menu=launcherslot5cascade)

	menubar.add_cascade(label="Launchers", menu=launchermenu)

	# Data menu+++++++++++++++
	datamenu=Menu(menubar, tearoff=0)

	dataslot1cascade=Menu(datamenu, tearoff=0)
	dataslot1cascade.add_command(label="Add Data Slot", command=m.addDataSlotSpec1)
	datamenu.add_cascade(label="Slot 1", menu=dataslot1cascade)

	dataslot2cascade=Menu(datamenu, tearoff=0)
	dataslot2cascade.add_command(label="Add Data Slot", command=m.addDataSlotSpec2)
	datamenu.add_cascade(label="Slot 2", menu=dataslot2cascade)

	dataslot3cascade=Menu(datamenu, tearoff=0)
	dataslot3cascade.add_command(label="Add Data Slot", command=m.addDataSlotSpec3)
	datamenu.add_cascade(label="Slot 3", menu=dataslot3cascade)

	dataslot4cascade=Menu(datamenu, tearoff=0)
	dataslot4cascade.add_command(label="Add Data Slot", command=m.addDataSlotSpec4)
	datamenu.add_cascade(label="Slot 4", menu=dataslot4cascade)

	dataslot5cascade=Menu(datamenu, tearoff=0)
	dataslot5cascade.add_command(label="Add Data Slot", command=m.addDataSlotSpec5)
	datamenu.add_cascade(label="Slot 5", menu=dataslot5cascade)

	menubar.add_cascade(label="Data Slots", menu=datamenu)

	#Backup menu++++++++++++++++(Some menu options are being replaced.)
	backupmenu=Menu(menubar, tearoff=0)
	#backupmenu.add_command(label="Backup one slot to file", command=m.empty)
	backupmenu.add_command(label="Backup all slots to file", command=m.empty)
	#backupmenu.add_command(label="Save launcher From list", command=m.empty)
	backupmenu.add_separator()
	#backupmenu.add_command(label="Import one slot", command=m.empty)
	backupmenu.add_command(label="Import all slots", command=m.empty)
	menubar.add_cascade(label="Backup", menu=backupmenu)

	optionsmenu=Menu(menubar, tearoff=0)
	optionsmenu.add_command(label="Edit Launchers", command=m.empty)
	#optionsmenu.add_command(label="Edit Data Slots", command=m.empty)
	optionsmenu.add_command(label="Delete Data", command=m.rmDataDir)
	menubar.add_cascade(label="Options", menu=optionsmenu)

	helpmenu=Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About", command=m.empty)
	menubar.add_cascade(label="Help", menu=helpmenu)

# =====================================================

	controlFrame = Frame(mainwin)
	startLauncherBtn1 = Button(controlFrame, text="Start the Launcher", command=m.startlauncher)
	exitMineManBtn1 = Button(controlFrame, text="Exit", command = mainwin.destroy)	

	launcherFrame= Frame(mainwin)
	launcherLabel = Label(launcherFrame, text="Launchers available:")
	global LaunVar
	LaunVar=IntVar()
	## BEN! WRITE A DEFINITION TO TRY TO PASS THE VALUE SELECTED TO THE LAUNCHERS.
	Laun1=Radiobutton(launcherFrame, text="Launcher 1 Slot: ", variable=LaunVar, value=1)
	Laun2=Radiobutton(launcherFrame, text="Launcher 2 Slot: ", variable=LaunVar, value=2)
	Laun3=Radiobutton(launcherFrame, text="Launcher 3 Slot: ", variable=LaunVar, value=3)
	Laun4=Radiobutton(launcherFrame, text="Launcher 4 Slot: ", variable=LaunVar, value=4)
	Laun5=Radiobutton(launcherFrame, text="Launcher 5 Slot: ", variable=LaunVar, value=5)

	dataFrame = Frame(mainwin)
	dataLabel= Label(dataFrame, text="Data folders available: ")
	global DataVar
	DataVar=IntVar()
	Data1=Radiobutton(dataFrame, text="Data 1 Slot: ", variable=DataVar, value=1)
	Data2=Radiobutton(dataFrame, text="Data 2 Slot: ", variable=DataVar, value=2)
	Data3=Radiobutton(dataFrame, text="Data 3 Slot: ", variable=DataVar, value=3)
	Data4=Radiobutton(dataFrame, text="Data 4 Slot: ", variable=DataVar, value=4)
	Data5=Radiobutton(dataFrame, text="Data 5 Slot: ", variable=DataVar, value=5)


	controlFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
	startLauncherBtn1.pack(side=RIGHT, padx=5)
	exitMineManBtn1.pack(side =RIGHT, padx=5)

	launcherFrame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
	launcherLabel.pack(side=LEFT, pady=5)
	Laun1.pack(padx=20, pady=2, anchor=W)
	Laun2.pack(padx=20, pady=2, anchor=W)
	Laun3.pack(padx=20, pady=2, anchor=W)
	Laun4.pack(padx=20, pady=2, anchor=W)
	Laun5.pack(padx=20, pady=2, anchor=W)

	dataFrame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
	dataLabel.pack(side=LEFT, pady=5)
	Data1.pack(padx=20, pady=2, anchor=W)
	Data2.pack(padx=20, pady=2, anchor=W)
	Data3.pack(padx=20, pady=2, anchor=W)
	Data4.pack(padx=20, pady=2, anchor=W)
	Data5.pack(padx=20, pady=2, anchor=W)

	mainwin.config(menu=menubar)
	mainwin.mainloop()

mainprog()
print "MineMan has exited."