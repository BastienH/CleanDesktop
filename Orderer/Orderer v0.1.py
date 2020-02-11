#-------------------------------------------------------------------------------
# Name:        Clean Computer Files
# Purpose:     Orders desktop files according to file type
#
# Author:      bastien.harkins
#
# Created:     10/11/2018
# Copyright:   (c) bastien.harkins 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import datetime

import logging
import os
from os.path import join, basename, getmtime
from platform import system
from sys import argv
from tkinter import filedialog
from tkinter import *

import mytoolkit as tool
from file_extensions_general import *
from file_extensions_personal import *                                                                                                        ### Context info ###

#Where
source_dir = os.getcwd()

#What
def find_folder_from_string(string):
    string = str(string)
    candidate_folders = [] 

    for root, folders, _ in os.walk(r'C:\Users\NG8203C\Desktop'):
        #root = C:\Users\NG8203C\Desktop\Clean Desktop\lib\xml 
        #folder = ['dom', 'etree', 'parsers', 'sax']
        for folder in folders:
            if string.lower() in folder.lower():
                candidate_folders.append(join(root, folder))

    return candidate_folders

def define_folder_to_order():
    pass

def gui_folder_pick():
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    folder_chosen = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory to clean up')
    return folder_chosen


#Check if user already chose his folder in sys.argv, 
if len(sys.argv) > 1: #if several, join them as a string
    folder_to_find = ' '.join(sys.argv[1:])
    candidate_folders = find_folder_from_string(folder_to_find)
    if len(candidate_folders) == 0:
        print("No Match")
        exit()
    elif len(candidate_folders) == 1:
        print(f'Do you want order: {candidate_folders[0]} ?')
        if input() in ("y", '', 'yes', 'OK'):
            folder_to_order = candidate_folders[0]
    else:
        print("I found several matches: ")
        for index, folder in enumerate(candidate_folders):
            print(f"{index+1}) {folder}")
        chosen_folder_index = int(input())
        folder_to_order = candidate_folders[chosen_folder_index -1]

elif len(sys.argv) == 1: #if only 1 then choose from Folder picker
    folder_to_order = gui_folder_pick()




print(folder_to_order)
exit()
"""
if len(sys.argv) == 1:
    folder_to_order = input("What do you want to clean? \n\n")

if desktop_or_other in ("y", '', 'yes', 'OK'):                
    if system() == 'Windows':
        desktop = join(os.environ['USERPROFILE'], 'Desktop', '') 

    elif system() in ('Linux', 'Darwin'):
        desktop = join(os.path.expanduser('~'), 'Desktop', '')
else:
    openfiledialog()
"""
#When
now = datetime.datetime.now()
today = ''.join([str(now.year), f"{now.month:02d}", f"{now.day:02d}"]) #Creates a "today" variable of format YYYYMMDD

#Parameters
RECENT = 2
EXCEPTIONS = []
HARD_CLEAN = False

                                                                                                        ### LOG config ###
log_path = join(source_dir, "LOG", f'cleanup_{today}.log')
assert os.path.exists(join(source_dir, "LOG")), os.mkdir(join(source_dir, "LOG"))

log_formatter = "%(asctime)s:%(levelname)s:%(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=log_formatter)
logging.info("Start App ===>")
logging.info(f"Source Directory: {source_dir}")
logging.info(f"Desktop path: {desktop}")


def terminal_only():
    choice = input(f'Do you wish to use only termininal? y or n:')
    if choice =="y":
        return True
    else:
        return False
                                                                                                        ### Accessory Functions ###
def mkdirs(sorting_dict={}):
    
    """Create a directory in the desktop for each dictionary key"""
    
    assert type(sorting_dict) == dict, f"input should be dict, current type for {sorting_dict} is {type(sorting_dict)}"

    for dirs in sorting_dict.keys():
            dirs_path = join(desktop, dirs, "")
            if os.path.isdir(dirs_path) == False:
                os.mkdir(dirs_path)
                print(rf"New dir : {dirs_path}")

def ui_verify_sorting(sorting_dict, exceptions=[]):
    
    print(f"\nThe sorting is as follows:")
    for k, v in sorting_dict.items():
        print(f"\n{k} : {v}")
    validation = input("Is this the pattern ? Press Enter to continue")
    if validation == '':
        return True
    else:
        return False

    
def list_desk_files(exception_list=[]):
    """Listing full path of desktop files"""

    assert "desktop" in globals(), "No Desktop configured"
    
    files = []
    for item in os.listdir(desktop):
        item = join(desktop, item)
        if os.path.isfile(item) and item not in exception_list:
            files.append(item)
    return files

def user_output(ordered_files, unordered_files):
    from ctypes import windll
    Win = windll.user32
    
    if unordered_files != []:
        Win.MessageBoxW(0, "The file(s) " + '\n'.join(unordered_files) + f"\nhave not been removed from {basename(desktop)}", 1)
    else:
        pass

    if ordered_files == []:
        Win.MessageBoxW(0, "Desktop is already clean", "No Action Taken", 1)
        logging.info("Desktop was already clean")
    else:
        removed_files = str("Clean up of :\n\n" + '\n'.join(ordered_files) + " \n\ncompleted successfully")
        Win.MessageBoxW(0, removed_files, "Removed", 1)

def check_recently_modified(path):
    edit_timestamp = getmtime(path)
    edit_datetime = datetime.datetime.fromtimestamp(edit_timestamp)
    formatted_edit_datetime = edit_datetime.strftime("%d/%m/%Y @ %H:%M:%S")
    delta = edit_datetime - now
    if delta.days < RECENT:
        return (True, formatted_edit_datetime)
    else:
        return (False, formatted_edit_datetime)

def move_file_or_not(path):
    """just check if the file as recently modified, if it has, user has the choice, else, we move"""
    recently_modified, formatted_edit_datetime = check_recently_modified(path)

    if recently_modified:
        choice = input(f' {basename(path).upper()} has been modified on {formatted_edit_datetime} \n'
            f'Do you wish to remove it from {basename(desktop).upper()}? y or n:')
        if choice == 'y':
            return True
        else:
            return False
    else:
        return True

def move_file_specific_folder(src, dst):
    pass
                                                                                                    ### Main Function ###
def change_directory(src_fpaths=[], sorting_dict={}, exception_list=[]):
    """ This function renames desktop files to new folders as defined in the sorting_dict
Example structure of the input dictionary is :
{"images" : [".jpg", ".png"]} """
    
    if ui_verify_sorting(sorting_dict):
        print("Sorting validated")
    else:
        print("CLEAN-UP CANCELLED")
        exit()
    
    #Making required directories
    mkdirs(sorting_dict)

    for src_fpath in src_fpaths:
        src_fpath_lower = src_fpath.lower()  #Setting src_fpath name to lower case for better comparison
        fname = basename(src_fpath)

        if move_file_or_not(src_fpath): #Let the user choose if files are moved individualy (for RECENT files) 
            pass
        else:
            unordered_files.append(fname)
            logging.info(logging.info(f"NOT MOVED {os.path.basename(desktop)}\{fname}"))
            continue        
        
        for destination, extensions in sorting_dict.items(): #Looping through input dictionary
            
            assert type(extensions) == list, f"Extensions should be presented in a list [], current value is {extension}"

            dst_dir = join(desktop, destination)
            dst_fpath = join(desktop, destination, fname)
            
            for ext in extensions: #Looping through the list of extensions
                
                assert type(ext) == str, f"Extensions should be strings, not {ext} that is of type {type(ext)}"
                
                if src_fpath_lower.endswith(ext.lower()):
                    #Now we rename the src_fpath to change their directory to destination  
                    try : 
                            os.rename(src_fpath, dst_fpath)
                            
                            #Adding the file name to the output list and writing log
                            ordered_files.append(fname)
                            logging.info(f"MOVED {os.path.basename(desktop)}\{fname} --> ..\{dst_dir}")

                    except FileExistsError:
                            dst_fpath = tool.file_num_increment(dst_fpath)
    
                            os.rename(src_fpath, dst_fpath)
                            f_new_name = os.path.basename(dst_fpath)

                            #Adding the new file name to the output list and writing log
                            ordered_files.append(f_new_name)
                            logging.info(f"MOVED(+1) {os.path.basename(desktop)}\{fname} --> ..\{dst_dir}\{f_new_name}")
                            continue

                    except PermissionError: #If the file is in use, user is warned.
                            unordered_files.append(fname)
                            logging.warning(f"{fname} not ordered: PermissionError.")
                            
                    except Exception as err:
                            error_msg = f"{fname}, it was probably not moved"\
                                        f"\n Error:{str(err)}"
                            logging.error(error_msg)

                        


                                                                                                                ### Main ###
if __name__ == "__main__":
    logging.info("Start Clean --->")
    ordered_files =  []
    unordered_files = []
    
    #change_directory(list_desk_files(), file_categories, exception_list=["cleaner.lnk"])
    change_directory(list_desk_files(), file_categories_personal_dict, exception_list=EXCEPTIONS)

    logging.info("---> End Clean")

    user_output(ordered_files, unordered_files)
    logging.info("===> End App")

