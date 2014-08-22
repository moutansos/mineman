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
import zipfile

osName = "Windows"
home_dir = os.path.expanduser("~")
data_dir = os.getenv('APPDATA') + "\\mineman"
cfg_main = ConfigParser.SafeConfigParser()
cfg_main.read(data_dir + "\\main.conf")


class M(object):
    def __init__(self):
        pass

    def empty(self):
        print "Unimplimented option."

    def zip_folder(self, folder_path, output_path):
        """Zip the contents of an entire folder (with that folder included
        in the archive). Empty subfolders will be included in the archive
        as well.
        """
        global zip_file
        parent_folder = os.path.dirname(folder_path)
        # Retrieve the paths of the folder contents.
        contents = os.walk(folder_path)
        try:
            zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
            for root, folders, files in contents:
                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    relative_path = absolute_path.replace(parent_folder + '\\',
                                                          '')
                    print "Adding '%s' to archive." % absolute_path
                    zip_file.write(absolute_path, relative_path)
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(parent_folder + '\\',
                                                          '')
                    print "Adding '%s' to archive." % absolute_path
                    zip_file.write(absolute_path, relative_path)
            print "'%s' created successfully." % output_path
        except IOError, message:
            print message
            sys.exit(1)
        except OSError, message:
            print message
            sys.exit(1)
        except zipfile.BadZipfile, message:
            print message
            sys.exit(1)
        finally:
            zip_file.close()

    # # BACKEND FUNCTIONS ====================================

    def start_file_management_thread(self):
        # Space for multithreading for file management. Provides a better and more stable way to manage files
        self.empty()

    def start_launcher(self):
        print "Running file and variable checks..."
        cfg_main.read(data_dir + "\\main.conf")
        launcherslot = ""
        data_slot = ""
        taskfail = 0
        try:
            launcherslot = str(LaunVar.get())
            if launcherslot == "0":
                raise
            else:
                pass
            print "Launcher specified is in slot " + launcherslot
            launtostart = cfg_main.get("launchers", "slot" + launcherslot)
        except:
            print "ERROR: No launcher specified."
            taskfail = 1

        try:
            data_slot = str(DataVar.get())
            if data_slot == "0":
                raise Exception("Invalid Data Slot")
            elif int(data_slot) < 0 or int(data_slot) > 5:
                pass
            elif data_slot == "6":
                data_slot = "original"
            else:
                print "ERROR. The config file seems to be not configured correctly."
            dattostart = cfg_main.get("data", "slot" + data_slot)
            print "Data specified is in slot " + data_slot

        except:
            print "ERROR: No data specified."
            taskfail = 1

        if taskfail == 1:
            print "Starting failed."
        else:
            print launtostart
            if launtostart == "<blank>":
                print "ERROR: No launcher is in that slot!"
            else:
                print data_slot
                if dattostart == "<Empty>":
                    print "ERROR: No data in that slot!"
                else:
                    try:
                        print "Clearing data out of the way... (INCLUDING DATA NOT SAVED IN BACKUP)"
                        shutil.rmtree(home_dir + "\\AppData\\Roaming\\.minecraft")
                    except:
                        pass
                    shutil.copytree(data_dir + "\\dataslots\\slot" + data_slot + "\\.minecraft",
                                    home_dir + "\\AppData\\Roaming\\.minecraft")
                    print "Starting launcher..."
                    os.system(launtostart)
                    print "Launcher stopped."
                    print "Moving back data..."
                    shutil.rmtree(data_dir + "\\dataslots\\slot" + data_slot + "\\.minecraft")
                    shutil.copytree(home_dir + "\\AppData\\Roaming\\.minecraft",
                                    data_dir + "\\dataslots\\slot" + data_slot + "\\.minecraft")
                    shutil.rmtree(home_dir + "\\AppData\\Roaming\\.minecraft")

    # # ----- SLOT SPECIFIC FUNCITONS.
    def addLauncherSlotSpec(self, launchnum):
        # Add safegaurds for slots already filled.
        print "Adding launcher to Slot " + launchnum
        launtoadd = askopenfilename()
        if launtoadd == "":
            print "ERROR: No file specified. Aborting launcher add."
        else:
            print "Launcher file specified: " + launtoadd
            LaunName = ""

            def getNameFromDiag():
                LaunName = GNDmainEntry.get()

                print "Launcher Name: " + LaunName
                if LaunName == "":
                    print "ERROR: No name was specified"
                else:
                    getNameDiag.destroy()
                    lauchnumLong = "slot" + launchnum

                    print "Copying launcher to launcher directory."
                    shutil.copyfile(launtoadd, data_dir + "\\launchers\\slot" + launchnum + ".jar")

                    cfg_main.set("launchers", lauchnumLong, data_dir + "\\launchers\\slot" + launchnum + ".jar")
                    cfg_main.set("launchers", lauchnumLong + "Name", LaunName)
                    print "Saving changes to config file."
                    with open(data_dir + "\\main.conf", 'wb') as configfile:
                        cfg_main.write(configfile)
                    # exec("Data"+launchnum+".config('text="+LaunName+"')")
                    if launchnum == "1":
                        Laun1.config(text="Launcher 1 Slot:     " + LaunName)
                    elif launchnum == "2":
                        Laun2.config(text="Launcher 2 Slot:     " + LaunName)
                    elif launchnum == "3":
                        Laun3.config(text="Launcher 3 Slot:     " + LaunName)
                    elif launchnum == "4":
                        Laun4.config(text="Launcher 4 Slot:     " + LaunName)
                    elif launchnum == "5":
                        Laun5.config(text="Launcher 5 Slot:     " + LaunName)
                    else:
                        print "INTERNAL ERROR: Not quite sure what happened, but the gui could not be updated."

            getNameDiag = Tk()
            getNameDiag.title("Input Launcher Name")
            GNDmainLabel = Label(getNameDiag, text="Please input a launcher name: ")
            GNDmainEntry = Entry(getNameDiag, text="")
            GNDmainButton = Button(getNameDiag, text="Ok", command=getNameFromDiag)
            GNDmainLabel.pack(padx=20, pady=10)
            GNDmainEntry.pack(padx=20, pady=10, fill=X)
            GNDmainButton.pack(padx=20, pady=10)
            getNameDiag.mainloop()

    def renameLauncherSlotSpec(self, launchnum):
        print "Renaming launcher " + launchnum
        cfg_main.read(data_dir + "\\main.conf")
        if cfg_main.get("launchers", "slot" + launchnum + "Name") == "<Empty>":
            print "Empty Slot! You can't rename an empty slot!"
        else:

            def GRWSRL():
                cfg_main.read(data_dir + "\\main.conf")
                if cfg_main.get("launchers", "slot" + launchnum) == "<blank>":
                    print "You can't rename an empty slot!"
                else:
                    nametochangeto = GRWmainEntry.get()
                    if nametochangeto == "<Empty>":
                        print "ERROR: You cant use that name."
                    else:
                        GRWmain.destroy()
                        cfg_main.set("launchers", "slot" + launchnum + "Name", nametochangeto)
                        with open(data_dir + "\\main.conf", 'wb') as configfile:
                            cfg_main.write(configfile)
                        print "Name is changed."
                        if launchnum == "1":
                            Laun1.config(text="Launcher 1 Slot:     " + nametochangeto)
                        elif launchnum == "2":
                            Laun2.config(text="Launcher 2 Slot:     " + nametochangeto)
                        elif launchnum == "3":
                            Laun3.config(text="Launcher 3 Slot:     " + nametochangeto)
                        elif launchnum == "4":
                            Laun4.config(text="Launcher 4 Slot:     " + nametochangeto)
                        elif launchnum == "5":
                            Laun5.config(text="Launcher 5 Slot:     " + nametochangeto)
                        else:
                            print "INTERNAL ERROR: Not quite sure what happened, but the gui could not be updated."

            GRWmain = Tk()
            GRWmain.title("New name")
            GRWmainLabel = Label(GRWmain, text="Please specify the new name for launcher " + launchnum)
            GRWmainEntry = Entry(GRWmain)
            GRWmainBtn = Button(GRWmain, text="Ok", command=GRWSRL)
            GRWmainLabel.pack(padx=10, pady=2)
            GRWmainEntry.pack(expand=1, padx=10, pady=2)
            GRWmainBtn.pack(padx=10, pady=2)
            GRWmain.mainloop()

    def deleteLauncherSlotSpec(self, launchnum):
        print "Deleting launcher " + launchnum
        cfg_main.read(data_dir + "\\main.conf")
        if cfg_main.get("launchers", "slot" + launchnum) == "<blank>":
            print "This slot is empty! You can't delete an empty slot!"
        else:
            def GDSADS():
                GDSmain.destroy()
                cfg_main.set("launchers", "slot" + launchnum, "<blank>")
                cfg_main.set("launchers", "slot" + launchnum + "Name", "<Empty>")
                with open(data_dir + "\\main.conf", 'wb') as configfile:
                    cfg_main.write(configfile)
                os.remove(data_dir + "\\launchers\\slot" + launchnum + ".jar")
                if launchnum == "1":
                    Laun1.config(text="Launcher 1 Slot:      <Empty>")
                elif launchnum == "2":
                    Laun2.config(text="Launcher 2 Slot:      <Empty>")
                elif launchnum == "3":
                    Laun3.config(text="Launcher 3 Slot:      <Empty>")
                elif launchnum == "4":
                    Laun4.config(text="Launcher 4 Slot:      <Empty>")
                elif launchnum == "5":
                    Laun5.config(text="Launcher 5 Slot:      <Empty>")
                else:
                    print "INTERNAL ERROR: Not quite sure what happened, but the gui could not be updated."

            def AbortDel():
                GDSmain.destroy()
                print "Aborting Delete."

            GDSmain = Tk()
            GDSmain.title("Delete this slot")
            GDSmainLabel = Label(GDSmain, text="Are you sure you want to delete slot" + launchnum + "?")

            GDSyesBtn = Button(GDSmain, text="Yes", command=GDSADS)
            GDSnoBtn = Button(GDSmain, text="No", command=AbortDel)

            GDSmainLabel.pack(padx=10, pady=2)
            GDSyesBtn.pack(fill=X, padx=10, pady=2)
            GDSnoBtn.pack(fill=X, padx=10, pady=2)

            GDSmain.mainloop()

    def addDataSlotSpec(self, datanum):
        # # This is the add data function that is working now!
        # Add tagging of new minecraft data direcctories. (Just a file)
        # Also add safegaurds so data does not get overwritten.
        print "Adding a new data slot."

        def writeData():
            AOWSmain.destroy()

            def getSlotFromDiag():
                DataName = ADSmainEntry.get()
                if DataName == "":
                    print "ERROR: No name was specified."
                else:
                    addDataWin.destroy()
                    slotNumber = "slot" + datanum + "Name"

                    def updateDataGUI():
                        if datanum == "1":
                            Data1.config(text="Data 1 Slot:     " + DataName)
                        elif datanum == "2":
                            Data2.config(text="Data 2 Slot:     " + DataName)
                        elif datanum == "3":
                            Data3.config(text="Data 3 Slot:     " + DataName)
                        elif datanum == "4":
                            Data4.config(text="Data 4 Slot:     " + DataName)
                        elif datanum == "5":
                            Data5.config(text="Data 5 Slot:     " + DataName)
                        else:
                            print "INTERNAL ERROR: Not quite sure what happened, but the gui could not be updated."

                    def newDataSlot():
                        ANOOmainWin.destroy()
                        try:
                            shutil.rmtree(data_dir + "\\dataslots\\slot" + datanum + "\\.minecraft")
                            print "There's data in this slot. It's been removed."
                        except:
                            pass
                        os.mkdir(data_dir + "\\dataslots\\slot" + datanum + "\\.minecraft")
                        cfg_main.set("data", slotNumber, DataName)
                        print "Saving changes to config file."
                        with open(data_dir + "\\main.conf", 'wb') as configfile:
                            cfg_main.write(configfile)
                        updateDataGUI()

                    def oldDataSlot():
                        ANOOmainWin.destroy()
                        datatoget = askdirectory()
                        try:
                            shutil.rmtree(data_dir + "\\dataslots\\slot" + datanum + "\\.minecraft")
                            print "There's data in this slot. It's been removed."
                        except:
                            pass
                        print "Copying data directory..."
                        shutil.copytree(datatoget, data_dir + "\\dataslots\\slot" + datanum + "\\.minecraft")
                        cfg_main.set("data", slotNumber, DataName)
                        print "Saving changes to config file."
                        with open(data_dir + "\\main.conf", 'wb') as configfile:
                            cfg_main.write(configfile)
                        updateDataGUI()

                    ANOOmainWin = Tk()
                    ANOOmainWin.title("New slot or choose data file?")
                    ANOOmainLabel = Label(ANOOmainWin,
                                          text="Is this a new slot or do you have old mineraft data for this slot?")
                    ANOOnewBtn = Button(ANOOmainWin, text="New", command=newDataSlot)
                    ANOOoldBtn = Button(ANOOmainWin, text="Old", command=oldDataSlot)
                    ANOOmainLabel.pack(padx=20, pady=10)
                    ANOOnewBtn.pack(padx=20, pady=10)
                    ANOOoldBtn.pack(padx=20, pady=10)
                    ANOOmainWin.mainloop()

            addDataWin = Tk()
            addDataWin.title("Specify a name for this slot.")
            ADSmainLabel = Label(addDataWin, text="Please specify a name for this data slot: ")
            ADSmainEntry = Entry(addDataWin)
            ADSmainButton = Button(addDataWin, text="Ok", command=getSlotFromDiag)
            ADSmainLabel.pack(padx=20, pady=10)
            ADSmainEntry.pack(padx=20, pady=10, fill=X)
            ADSmainButton.pack(padx=20, pady=10)
            addDataWin.mainloop()

        def AbortNewData():
            AOWSmain.destroy()
            print "Aborting creating or writing a new data slot."

        cfg_main.read(data_dir + "\\main.conf")
        if cfg_main.get("data", "slot" + datanum + "Name") == "<Empty>":
            print "Using empty slot."
        else:
            print "WARNING: There's data there!"
        AOWSmain = Tk()
        AOWSmain.title("Overwright this slot")
        AOWSmainLabel = Label(AOWSmain, text="Are you sure you want to overwright slot" + datanum + "?")

        AOWSyesBtn = Button(AOWSmain, text="Yes", command=writeData)
        AOWSnoBtn = Button(AOWSmain, text="No", command=AbortNewData)

        AOWSmainLabel.pack(padx=10, pady=2)
        AOWSyesBtn.pack(fill=X, padx=10, pady=2)
        AOWSnoBtn.pack(fill=X, padx=10, pady=2)
        AOWSmain.mainloop()

    def renameDataSlotSpec(self, datanum):
        print "Renaming data..."
        cfg_main.read(data_dir + "\\main.conf")
        if cfg_main.get("data", "slot" + datanum + "Name") == "<Empty>":
            print "You can't rename an empty data slot!"
        else:
            def GRDS():
                nametochangeto = GRDmainEntry.get()
                if nametochangeto == "<Empty>":
                    print "You can't use that name sorry."
                else:
                    GRDmain.destroy()
                    print "Renaming data slot " + datanum
                    cfg_main.set("data", "slot" + datanum + "Name", nametochangeto)
                    with open(data_dir + "\\main.conf", 'wb') as configfile:
                        cfg_main.write(configfile)
                    print "Name is changed."
                    if datanum == "1":
                        Data1.config(text="Data 1 Slot:     " + nametochangeto)
                    elif datanum == "2":
                        Data2.config(text="Data 2 Slot:     " + nametochangeto)
                    elif datanum == "3":
                        Data3.config(text="Data 3 Slot:     " + nametochangeto)
                    elif datanum == "4":
                        Data4.config(text="Data 4 Slot:     " + nametochangeto)
                    elif datanum == "5":
                        Data5.config(text="Data 5 Slot:     " + nametochangeto)
                    else:
                        print "INTERNAL ERROR: Not quite sure what happened, but the gui could not be updated."

            GRDmain = Tk()
            GRDmain.title("Rename data slot")
            GRDmainLabel = Label(GRDmain, text="Provide a new name for slot number " + datanum)
            GRDmainEntry = Entry(GRDmain)
            GRDmainBtn = Button(GRDmain, text="Ok", command=GRDS)
            GRDmainLabel.pack(padx=10, pady=2)
            GRDmainEntry.pack(expand=1, padx=10, pady=2)
            GRDmainBtn.pack(padx=10, pady=2)
            GRDmain.mainloop()

    def deleteDataSlotSpec(self, datanum):
        self.empty

    # # END SLOT SPECIFIC FUNCTIONS.

    def backupOriginal(self):
        # Add warning if the orignal is a mineman slot.
        print "Backing up original minecraft data."

        def backupTheOriginal():
            print "Copying folder...."
            try:
                shutil.copytree(home_dir + "\\AppData\\Roaming\\.minecraft",
                                data_dir + "\\dataslots\\slotoriginal\\.minecraft")
                print "Removing original directory..."
                shutil.rmtree(home_dir + "\\AppData\\Roaming\\.minecraft")

                cfg_main.read(data_dir + "\\main.cfg")
                cfg_main.set("data", "slotoriginal", "<yes>")
                with open(data_dir + "\\main.conf", 'wb') as configfile:
                    cfg_main.write(configfile)
                DataOrigin.config(text="Original Slot:     <Filled>")
            except:
                print "An eror occured backing up the original minecraft data. Is there any data to back up?"

            print "Finished."

        cfg_main.read(data_dir + "\\main.cfg")
        if cfg_main.get("data", "slotoriginal") == "<yes>":
            print "The original backup slot is already filled."
        else:
            print "Backup slot clear."
            backupTheOriginal()

    def restoreOriginal(self):
        print "Restoring original..."
        cfg_main.read(data_dir + "\\main.cfg")
        if cfg_main.get("data", "slotoriginal") == "<no>":
            print "You can't restore the original data folder... You never made a backup!"
        elif cfg_main.get("data", "slotoriginal") == "<yes>":
            print "Proceeding..."
            try:
                try:
                    shutil.rmtree(home_dir + "\\AppData\\Roaming\\.minecraft")
                    print "Cleared the space..."
                except:
                    pass
                shutil.copytree(data_dir + "\\dataslots\\slotoriginal\\.minecraft",
                                home_dir + "\\AppData\\Roaming\\.minecraft")
                print "Restored."
            except:
                print "An error occured."
        else:
            print "There was an error. The config file might be misconfigured or nonexistent."

    def deleteOriginal(self):
        m.empty()

    def exitProg(self):
        print "Exiting program...."
        main_win.destroy()

    def rmDataDir(self):
        print "Removing data directory..."

        def clear():
            askClearAll.destroy()
            shutil.rmtree(data_dir)
            print "Directory removed."

        def abort():
            askClearAll.destroy()
            print "Delete was canceled."

        askClearAll = Tk()
        askClearAll.title("Are you sure?")
        acaMainLabel = Label(askClearAll, text="Are you sure you want to clear the entire data directory?")
        acaSecondLabel = Label(askClearAll,
                               text="(This cannot be undone and it will delete your original minecraft data.)")
        acaYesBtn = Button(askClearAll, text="Yes", command=clear)
        acaNoBtn = Button(askClearAll, text="No", command=abort)
        acaMainLabel.pack(padx=10, pady=2)
        acaSecondLabel.pack(padx=10, pady=2)
        acaYesBtn.pack(fill=X, padx=10, pady=2)
        acaNoBtn.pack(fill=X, padx=10, pady=2)
        askClearAll.mainloop()

    def rmMinecraftDir(self):
        print "Removing Minecraft data directory..."

        def clear():
            askClearAll.destroy()
            shutil.rmtree(home_dir + "\\AppData\\Roaming\\.minecraft")
            print "Directory removed."

        def abort():
            askClearAll.destroy()
            print "Delete was canceled."

        askClearAll = Tk()
        askClearAll.title("Are you sure?")
        acaMainLabel = Label(askClearAll, text="Are you sure you want to clear the entire Minecraft data directory?")
        acaSecondLabel = Label(askClearAll,
                               text="(This cannot be undone and it will delete your"
                                    " minecraft data if any is stored in the original folder.)")
        acaYesBtn = Button(askClearAll, text="Yes", command=clear)
        acaNoBtn = Button(askClearAll, text="No", command=abort)
        acaMainLabel.pack(padx=10, pady=2)
        acaSecondLabel.pack(padx=10, pady=2)
        acaYesBtn.pack(fill=X, padx=10, pady=2)
        acaNoBtn.pack(fill=X, padx=10, pady=2)
        askClearAll.mainloop()

    def makeDataDir(self):
        print "Creating a new data directory..."
        os.makedirs(data_dir)
        os.makedirs(data_dir + "\\launchers")
        os.makedirs(data_dir + "\\dataslots")
        os.makedirs(data_dir + "\\dataslots\slot1")
        os.makedirs(data_dir + "\\dataslots\slot2")
        os.makedirs(data_dir + "\\dataslots\slot3")
        os.makedirs(data_dir + "\\dataslots\slot4")
        os.makedirs(data_dir + "\\dataslots\slot5")
        os.makedirs(data_dir + "\\dataslots\slotoriginal")
        shutil.copyfile("default.conf", data_dir + "\\main.conf")
        print "Created sucessfuly.\n"

    # STARTUP FUNCTIONS ==========================================================

    def startupChecks(self):
        if osName == "Windows":
            if not os.path.exists(data_dir):
                print "Data directory not found."
                self.makeDataDir()
                print "Data directories created. If program fails please restart."
            else:
                pass
        else:
            print "Error. No data directory could be found due to unknown OS. " \
                  "Data directory being written in program folder."

        print cfg_main.get("startup", "version")
        if cfg_main.get("startup", "debug") == "yes":
            debug1 = 1
        else:
            debug1 = 0

        try:
            print "\n Loading launchers from config..."
            launcher1 = cfg_main.get("launchers", "slot1")
            launcher1Name = cfg_main.get("launchers", "slot1Name")
            print "Launcher1 Loaded"
            launcher2 = cfg_main.get("launchers", "slot2")
            launcher2Name = cfg_main.get("launchers", "slot2Name")
            print "Launcher2 Loaded"
            launcher3 = cfg_main.get("launchers", "slot3")
            launcher3Name = cfg_main.get("launchers", "slot3Name")
            print "Launcher3 Loaded"
            launcher4 = cfg_main.get("launchers", "slot4")
            launcher4Name = cfg_main.get("launchers", "slot4Name")
            print "Launcher4 Loaded"
            launcher5 = cfg_main.get("launchers", "slot5")
            launcer5Name = cfg_main.get("launchers", "slot5Name")
            print "Launcher5 Loaded"
            print " All launchers loaded sucessfuly.\n\n Proceeding to load data slots."

            data1 = cfg_main.get("data", "slot1Name")
            print "Dataslot1 Loaded."
            data2 = cfg_main.get("data", "slot2Name")
            print "Dataslot2 Loaded."
            data3 = cfg_main.get("data", "slot3Name")
            print "Dataslot3 Loaded."
            data4 = cfg_main.get("data", "slot4Name")
            print "DataSlot4 Loaded."
            data5 = cfg_main.get("data", "slot5Name")
            print "Dataslot5 Loaded.\n All dataslots sucessfuly loaded.\n\n"
        except:
            print "One or more config values was not found. " \
                  "Program will probably crash. Delete datafolder and start over."


m = M()


def exit2():
    sys.exit()


def mainprog():
    print "Starting MineMan 1.0....."
    print ""
    m.startupChecks()
    print ""
    print "Currently this program is a work in progress. \nSome features may not be implimented yet.\n\n"
    global main_win
    main_win = Tk()
    main_win.title("MineMan 1.0")
    main_win.geometry("500x350")

    # Menu Funcitons ======================================
    menubar = Menu(main_win)

    filemenu = Menu(menubar, tearoff=0)
    # filemenu.add_command(label="Add a Launcher", command=m.empty)
    # filemenu.add_command(label="Save Config", command=m.empty)
    # filemenu.add_separator()
    filemenu.add_command(label="Exit", command=main_win.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    # Launcher menu++++++++++++
    launchermenu = Menu(menubar, tearoff=0)

    launcherslot1cascade = Menu(launchermenu, tearoff=0)
    launcherslot1cascade.add_command(label="Add Launcher", command=lambda: m.addLauncherSlotSpec("1"))
    launcherslot1cascade.add_command(label="Rename Launcher", command=lambda: m.renameLauncherSlotSpec("1"))
    launcherslot1cascade.add_command(label="Clear Launcher", command=lambda: m.deleteLauncherSlotSpec("1"))
    launchermenu.add_cascade(label="Slot 1", menu=launcherslot1cascade)

    launcherslot2cascade = Menu(launchermenu, tearoff=0)
    launcherslot2cascade.add_command(label="Add Launcher", command=lambda: m.addLauncherSlotSpec("2"))
    launcherslot2cascade.add_command(label="Rename Launcher", command=lambda: m.renameLauncherSlotSpec("2"))
    launcherslot2cascade.add_command(label="Clear Launcher", command=lambda: m.deleteLauncherSlotSpec("2"))
    launchermenu.add_cascade(label="Slot 2", menu=launcherslot2cascade)

    launcherslot3cascade = Menu(launchermenu, tearoff=0)
    launcherslot3cascade.add_command(label="Add Launcher", command=lambda: m.addLauncherSlotSpec("3"))
    launcherslot3cascade.add_command(label="Rename Launcher", command=lambda: m.renameLauncherSlotSpec("3"))
    launcherslot3cascade.add_command(label="Clear Launcher", command=lambda: m.deleteLauncherSlotSpec("3"))
    launchermenu.add_cascade(label="Slot 3", menu=launcherslot3cascade)

    launcherslot4cascade = Menu(launchermenu, tearoff=0)
    launcherslot4cascade.add_command(label="Add Launcher", command=lambda: m.addLauncherSlotSpec("4"))
    launcherslot4cascade.add_command(label="Rename Launcher", command=lambda: m.renameLauncherSlotSpec("4"))
    launcherslot4cascade.add_command(label="Clear Launcher", command=lambda: m.deleteLauncherSlotSpec("4"))
    launchermenu.add_cascade(label="Slot 4", menu=launcherslot4cascade)

    launcherslot5cascade = Menu(launchermenu, tearoff=0)
    launcherslot5cascade.add_command(label="Add Launcher", command=lambda: m.addLauncherSlotSpec("5"))
    launcherslot5cascade.add_command(label="Rename Launcher", command=lambda: m.renameLauncherSlotSpec("5"))
    launcherslot5cascade.add_command(label="Clear Launcher", command=lambda: m.deleteLauncherSlotSpec("5"))
    launchermenu.add_cascade(label="Slot 5", menu=launcherslot5cascade)

    menubar.add_cascade(label="Launchers", menu=launchermenu)

    # Data menu+++++++++++++++
    datamenu = Menu(menubar, tearoff=0)

    dataslot1cascade = Menu(datamenu, tearoff=0)
    dataslot1cascade.add_command(label="Add Data Slot", command=lambda: m.addDataSlotSpec("1"))
    dataslot1cascade.add_command(label="Rename Data Slot", command=lambda: m.renameDataSlotSpec("1"))
    dataslot1cascade.add_command(label="Clear Data Slot", command=lambda: m.deleteDataSlotSpec("1"))
    datamenu.add_cascade(label="Slot 1", menu=dataslot1cascade)

    dataslot2cascade = Menu(datamenu, tearoff=0)
    dataslot2cascade.add_command(label="Add Data Slot", command=lambda: m.addDataSlotSpec("2"))
    dataslot2cascade.add_command(label="Rename Data Slot", command=lambda: m.renameDataSlotSpec("2"))
    dataslot2cascade.add_command(label="Clear Data Slot", command=lambda: m.deleteDataSlotSpec("2"))
    datamenu.add_cascade(label="Slot 2", menu=dataslot2cascade)

    dataslot3cascade = Menu(datamenu, tearoff=0)
    dataslot3cascade.add_command(label="Add Data Slot", command=lambda: m.addDataSlotSpec("3"))
    dataslot3cascade.add_command(label="Rename Data Slot", command=lambda: m.renameDataSlotSpec("3"))
    dataslot3cascade.add_command(label="Clear Data Slot", command=lambda: m.deleteDataSlotSpec("3"))
    datamenu.add_cascade(label="Slot 3", menu=dataslot3cascade)

    dataslot4cascade = Menu(datamenu, tearoff=0)
    dataslot4cascade.add_command(label="Add Data Slot", command=lambda: m.addDataSlotSpec("4"))
    dataslot4cascade.add_command(label="Rename Data Slot", command=lambda: m.renameDataSlotSpec("4"))
    dataslot4cascade.add_command(label="Clear Data Slot", command=lambda: m.deleteDataSlotSpec("4"))
    datamenu.add_cascade(label="Slot 4", menu=dataslot4cascade)

    dataslot5cascade = Menu(datamenu, tearoff=0)
    dataslot5cascade.add_command(label="Add Data Slot", command=lambda: m.addDataSlotSpec("5"))
    dataslot5cascade.add_command(label="Rename Data Slot", command=lambda: m.renameDataSlotSpec("5"))
    dataslot5cascade.add_command(label="Clear Data Slot", command=lambda: m.deleteDataSlotSpec("5"))
    datamenu.add_cascade(label="Slot 5", menu=dataslot5cascade)

    menubar.add_cascade(label="Data Slots", menu=datamenu)

    # Backup menu++++++++++++++++(Some menu options are being replaced.)
    backupmenu = Menu(menubar, tearoff=0)
    backupmenu.add_command(label="Backup original minecraft data", command=m.backupOriginal)
    backupmenu.add_command(label="Restore original minecraft data", command=m.restoreOriginal)
    # backupmenu.add_command(label="Backup one slot to file", command=m.empty)
    # backupmenu.add_command(label="Save launcher From list", command=m.empty)
    backupmenu.add_separator()
    # backupmenu.add_command(label="Import one slot", command=m.empty)
    backupmenu.add_command(label="Backup all slots to file", command=m.empty)
    backupmenu.add_command(label="Import all slots", command=m.empty)
    #backupmenu.add_command(label="Restore original minecraft data", command=m.restoreOriginal)
    menubar.add_cascade(label="Backup", menu=backupmenu)

    optionsmenu = Menu(menubar, tearoff=0)
    #optionsmenu.add_command(label="Edit Launchers", command=m.empty)
    #optionsmenu.add_command(label="Edit Data Slots", command=m.empty)
    optionsmenu.add_command(label="Delete Mineman Data", command=m.rmDataDir)
    optionsmenu.add_command(label="Delete Minecraft Data", command=m.rmMinecraftDir)
    menubar.add_cascade(label="Options", menu=optionsmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=m.empty)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # =====================================================

    controlFrame = Frame(main_win)
    startLauncherBtn1 = Button(controlFrame, text="Start the Launcher", command=m.start_launcher)
    exitMineManBtn1 = Button(controlFrame, text="Exit", command=main_win.destroy)

    launcherFrame = Frame(main_win)
    launcherLabel = Label(launcherFrame, text="Launchers available:")
    cfg_main.read(data_dir + "\\main.conf")
    launcherslot1Name = cfg_main.get("launchers", "slot1Name")
    launcherslot2Name = cfg_main.get("launchers", "slot2Name")
    launcherslot3Name = cfg_main.get("launchers", "slot3Name")
    launcherslot4Name = cfg_main.get("launchers", "slot4Name")
    launcherslot5Name = cfg_main.get("launchers", "slot5Name")
    global LaunVar
    global Laun1
    global Laun2
    global Laun3
    global Laun4
    global Laun5
    LaunVar = IntVar()
    ## BEN! WRITE A DEFINITION TO TRY TO PASS THE VALUE SELECTED TO THE LAUNCHERS.
    Laun1 = Radiobutton(launcherFrame, text="Launcher 1 Slot:     " + launcherslot1Name, variable=LaunVar, value=1)
    Laun2 = Radiobutton(launcherFrame, text="Launcher 2 Slot:     " + launcherslot2Name, variable=LaunVar, value=2)
    Laun3 = Radiobutton(launcherFrame, text="Launcher 3 Slot:     " + launcherslot3Name, variable=LaunVar, value=3)
    Laun4 = Radiobutton(launcherFrame, text="Launcher 4 Slot:     " + launcherslot4Name, variable=LaunVar, value=4)
    Laun5 = Radiobutton(launcherFrame, text="Launcher 5 Slot:     " + launcherslot5Name, variable=LaunVar, value=5)

    dataFrame = Frame(main_win)
    dataLabel = Label(dataFrame, text="Data folders available: ")
    dataslot1Name = cfg_main.get("data", "slot1Name")
    dataslot2Name = cfg_main.get("data", "slot2Name")
    dataslot3Name = cfg_main.get("data", "slot3Name")
    dataslot4Name = cfg_main.get("data", "slot4Name")
    dataslot5Name = cfg_main.get("data", "slot5Name")
    if cfg_main.get("data", "slotoriginal") == "<yes>":
        originalDataName = "<Filled>"
    else:
        originalDataName = "<Empty>"
    global DataVar
    global Data1
    global Data2
    global Data3
    global Data4
    global Data5
    global DataOrigin
    DataVar = IntVar()
    Data1 = Radiobutton(dataFrame, text="Data 1 Slot:     " + dataslot1Name, variable=DataVar, value=1)
    Data2 = Radiobutton(dataFrame, text="Data 2 Slot:     " + dataslot2Name, variable=DataVar, value=2)
    Data3 = Radiobutton(dataFrame, text="Data 3 Slot:     " + dataslot3Name, variable=DataVar, value=3)
    Data4 = Radiobutton(dataFrame, text="Data 4 Slot:     " + dataslot4Name, variable=DataVar, value=4)
    Data5 = Radiobutton(dataFrame, text="Data 5 Slot:     " + dataslot5Name, variable=DataVar, value=5)
    DataOrigin = Radiobutton(dataFrame, text="Original Slot:     " + originalDataName, variable=DataVar, value=6)

    controlFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    startLauncherBtn1.pack(side=RIGHT, padx=5)
    exitMineManBtn1.pack(side=RIGHT, padx=5)

    launcherFrame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
    launcherLabel.pack(side=LEFT, pady=5)
    Laun1.pack(padx=20, pady=1, anchor=W)
    Laun2.pack(padx=20, pady=1, anchor=W)
    Laun3.pack(padx=20, pady=1, anchor=W)
    Laun4.pack(padx=20, pady=1, anchor=W)
    Laun5.pack(padx=20, pady=1, anchor=W)

    dataFrame.pack(side=TOP, fill=BOTH, padx=5, pady=5)
    dataLabel.pack(side=LEFT, pady=5)
    Data1.pack(padx=20, pady=1, anchor=W)
    Data2.pack(padx=20, pady=1, anchor=W)
    Data3.pack(padx=20, pady=1, anchor=W)
    Data4.pack(padx=20, pady=1, anchor=W)
    Data5.pack(padx=20, pady=1, anchor=W)
    DataOrigin.pack(padx=20, pady=1, anchor=W)

    main_win.config(menu=menubar)
    main_win.mainloop()


mainprog()
print "MineMan has exited."