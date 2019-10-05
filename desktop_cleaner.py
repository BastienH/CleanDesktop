#-------------------------------------------------------------------------------
# Name:        desktop cleaner
# Purpose:     Orders desktop files according to type .
#
# Author:      bastien.harkins
#
# Created:     10/11/2018
# Copyright:   (c) bastien.harkins 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
from os.path import join as pjoin
import ctypes
import datetime
import platform
#from sys import last_traceback as log

"""This cleans up the Desktop folder (moving to Trash) all file in the list expendable_formats.
If it runs into docs that are in use, it skips."""

#Choose the expendanbles to be moved into TRASH
expendable_formats = ["png", "bat", "jpg", "msg", ".lnk", "html", "pptx", 'ico', 'txt', "oft", "docx", "doc", "zip", ".7z", "PNG", "emz", "pst", ".eml"]
pdf_files = ["pdf"]
executables = ["exe", "rdp"]
whl_files = ["whl"]
data_files = ["csv", "xlsx", "xls", "json", "xml", "evtx"]
script_files = [".py"]
video_files = [".mp4"]



#DESKTOP ...
operating_system = platform.system()

if operating_system == 'Windows':
    desktop = pjoin(os.environ['USERPROFILE'], 'Desktop', '') 

elif operating_system in ('Linux', 'Darwin'):
    desktop = pjoin(os.path.expanduser('~'), 'Desktop', '') 

    
#TRASH
trash = pjoin(desktop, "Trash", "")

#OTHER
installs = pjoin(desktop, "INSTALLS", "")
data = pjoin(desktop, "DATA", "")
whl = pjoin(desktop, "Python Packages", "")
scripts = pjoin(desktop, "Scripts", "")
pdf = pjoin(desktop, "PDFs", "")
videos = pjoin(desktop, "VIDEOS", "")

folders = [trash, installs, data, whl, scripts, pdf, videos]

for f in folders:
    if os.path.isdir(f) == False:
        os.mkdir(f)
    
#This list will be used for user output.
ordered_files =  []

#We get date in case of duplicates
now = datetime.datetime.now()
today = ''.join([str(now.year), f"{now.month:02d}", f"{now.day:02d}"]) #Creates a today variable of format YYYYMMDD

#not used YET
def log_file(error):
    logfile = desktop+"cleanup.log"
    log = open(logfile, 'w')
    log.write(error)
    log.close()


def change_directory(formats, destination):
    #Loop through the desktop directory
    for doc in os.listdir(desktop):
        doc = doc.lower()  #sets all to lower case 
        for f in formats :
                if doc.endswith(f) and doc != "cleaner.lnk":
                    try : #Rename the file to change their directory to destination (exepect the Cleaner shortcut)
                        os.rename(desktop+doc, destination+doc)
                        ordered_files.append(doc)
                        print("appended")

                    except FileExistsError: #We add the date of clean up
                        os.rename(desktop+doc, destination+today+doc)
                        ordered_files.append(doc)

                    except PermissionError: #If the doc is in use, user is warned.
                        ctypes.windll.user32.MessageBoxW(0, "The file" + doc + " is being used", "Not removed from desktop", 1)
                        
                    except Exception as err:
                        error = "Error caught while cleaning up" + doc + "@" + today + ". Error is : " + str(err)
                        log_file(error)
                        print("error caught")
    print("change successfull")
    

    #Run 
change_directory(expendable_formats, trash)
change_directory(executables, installs)
change_directory(data_files, data)
change_directory(whl_files, whl)
change_directory(script_files, scripts)
change_directory(pdf_files, pdf)
change_directory(video_files, videos)

#Pops up a window with the list of removed items.
if ordered_files == []:
    ctypes.windll.user32.MessageBoxW(0, "Desktop is already clean", "No Action Taken", 1)
else:
    removed_docs = str("Clean up of :\n\n" + '\n'.join(ordered_files) + " \n\ncompleted successfully")
    ctypes.windll.user32.MessageBoxW(0, removed_docs, "Removed", 1)



