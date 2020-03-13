#-------------------------------------------------------------------------------
# Name:        desktop cleaner
# Purpose:     Orders desktop files according to type .
#
# Author:      bastien.harkins
#
# Created:     10/11/2018
#-------------------------------------------------------------------------------

import datetime
import time
import os
import logging
from os.path import join, basename, getmtime
from platform import system

from mytoolkit import file_num_increment

import mapping


"""This script is used to order a messy directory. Typically a desktop.
What order you might say?
    Check out mapping.py
    Or run the present script and find out.

The target of future versions is to order recursively people's storage devices. See Orderer

Until I implement recursivity, this script is quite harmless...
It only runs in the requested folder.
"""

                                                                                                        ### Context info ###

#Where
source_dir = os.getcwd()

#What
print('Welcome, \n\nThis script is used to order a messy directory. \nTypically a desktop.')
print('\nWarning: Cleaning is not programmed to be undone automatically')
print('Use with care\n')

desktop_or_other = input("Do you want to clean the desktop (d) or other (o) : ")
if desktop_or_other in ("d", '', 'D', 'desktop', 'Desktop'):
    if system() == 'Windows':
        desktop = join(os.environ['USERPROFILE'], 'Desktop', '')

    elif system() in ('Linux', 'Darwin'):
        desktop = join(os.path.expanduser('~'), 'Desktop', '')
elif desktop_or_other in ("o", 'O', 'other', 'Other'):
    from tkinter import filedialog
    from tkinter import *
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    desktop = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory to clean up')
else:
    print("Cleaning cancelled")
    exit()

#When
now = datetime.datetime.now()
today = ''.join([str(now.year), f"{now.month:02d}", f"{now.day:02d}"]) #Creates a "today" variable of format YYYYMMDD

#Parameters
RECENT = 3 #Days
EXCEPTIONS = [".ICO"] #
HARD_CLEAN = False

                                                                                                        ### LOG config ###
log_path = join(source_dir, "LOG", f'cleanup_{today}.log')
if not os.path.exists(join(source_dir, "LOG")):
    os.mkdir(join(source_dir, "LOG"))

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

def ui_verify_sorting(maps, exceptions=[]):

    for i, map in enumerate(maps):
        print(f"\nOrder n°{i+1} :")
        print(f"\nFOLDERS            <= FILES")
        for k, v in map.items():
            time.sleep(0.08)
            print(f"{k:<18} <= {', '.join(v)}")
        input("Press any key to show more")

    choice = input("Select your order, or any other key to cancel :")
    try:
        choice = int(choice) - 1
        if choice in range(len(maps)):
            return maps[choice]
    except:
        print("Clean-up Cancelled")
        exit()

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
    """"""
    if unordered_files != []:
        print("\n\nThe file(s):\n" + '\n'.join(unordered_files) + " is/are being used\n\n")
    else:
        pass

    if ordered_files == []:
        print("\n\nDesktop is already clean\nNo Action Taken\n\n")
        logging.info("Desktop was already clean")
    else:
        print(str("\n\nClean up of :\n\n" + '\n'.join(ordered_files) + " \n\ncompleted successfully"))

def check_recently_modified(path:str) -> bool:
    """
    Returns a boolean checking if the file/dir has been modified recently (defined by the RECENT var)
    and returns the formatted_datetime of this modification.
    """
    edit_timestamp = getmtime(path)
    edit_datetime = datetime.datetime.fromtimestamp(edit_timestamp)
    formatted_edit_datetime = edit_datetime.strftime("%d/%m/%Y @ %H:%M:%S")
    delta = edit_datetime - now
    if abs(delta.days) <= RECENT:
        return True, formatted_edit_datetime
    else:
        return False, formatted_edit_datetime

def move_file_or_not(path:str) -> bool:
    """
    Check if the file as recently modified, if it has, user has the choice, else, we move
    """
    recently_modified, formatted_edit_datetime = check_recently_modified(path)

    if recently_modified:
        choice = input(f' {basename(path).upper()} has been modified on {formatted_edit_datetime} \n'
            f'Do you wish to remove it from {basename(desktop).upper()}? y or n:')
        if choice in ['y', '']:
            return True
        else:
            return False
    else:
        return True

def move_file_specific_folder(src, dst):
    pass

def create_new_structure(src_fpaths=[], sorting_dict={}, exception_list=[]):
    pass
    #Inspiration here : https://pythontips.com/2014/01/23/python-101-writing-a-cleanup-script/"

def rollback():
    """
    Current rollback can be applied by running the following python code in the dir where the ordering was applied,
    like so :
    
    MAP_NUM = 1 #Pick the order you had chosen
    import mapping
    dir_ = os.getcwd()
    dirs = list(mapping.available_maps[MAP_NUM].keys())
    dirs = [os.path.join(dir_, d) for d in dirs]
    from_dirs_to_dir(dirs, dir_, del_dirs=True)
    
    """
    pass

def from_dirs_to_dir(dirs, dir_, del_dirs=False)-> None:
    """   
    Groups files from differents directories into a single dir_.
    Dirs should be a list of fullpaths, dir_ is a target directory for all fils in the provided dirs
    """
    for d in dirs: #input full paths
        assert os.path.isdir(d), '{d} is not a directory'
        listdir = os.listdir(d)
        for item in listdir:
            item_fpath = join(d, item)
            target = join(dir_, item)
            os.rename(item_fpath, target)
        if del_dirs:
            os.rmdir(d)
        
def copy_dir_structure(dir, depth=None):
    pass

def apply_exceptions(maps):
    for m in maps: #For each map
        for type_list in m.values(): #For each list of types in the map
            for t in type_list: #For each file extension in the list
                #Upper all items for comparision
                if t.upper() in [e.upper() for e in EXCEPTIONS]: 
                    type_list.remove(t)
    return maps
                                                                                                    ### Main Function ###                  
def change_directory(src_fpaths=[], sorting_dict={}, exception_list=[]):
    """ This function renames desktop files to new folders as defined in the sorting_dict
Example structure of the input dictionary is :
{"images" : [".jpg", ".png"]} """

    #Making required directories
    mkdirs(sorting_dict)

    for src_fpath in src_fpaths:
        src_fpath_lower = src_fpath.lower()
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
                            dst_fpath = file_num_increment(dst_fpath)

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

    apply_exceptions(mapping.available_maps)
    
    mapping_dict = ui_verify_sorting(mapping.available_maps)
        
    ordered_files =  []
    unordered_files = []

    #change_directory(list_desk_files(), file_categories, exception_list=["cleaner.lnk"])
    change_directory(list_desk_files(), mapping_dict, exception_list=EXCEPTIONS)

    logging.info("---> End Clean")

    user_output(ordered_files, unordered_files)
    logging.info("===> End App")
