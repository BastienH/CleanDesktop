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

import datetime
import os
import logging
from os.path import join as pjoin
from os.path import basename as basename
from platform import system

#from file_extensions_general import *
from file_extensions_personal import *


"""This cleans up the Desktop folder based on file extension
If it runs into files that are in use, it skips."""    

                                                                                                        ### Context info ###

#Where
source_dir = os.getcwd()

#What
if system() == 'Windows':
    desktop = pjoin(os.environ['USERPROFILE'], 'Desktop', '') 

elif system() in ('Linux', 'Darwin'):
    desktop = pjoin(os.path.expanduser('~'), 'Desktop', '')
    
#When
now = datetime.datetime.now()
today = ''.join([str(now.year), f"{now.month:02d}", f"{now.day:02d}"]) #Creates a "today" variable of format YYYYMMDD




                                                                                                        ### LOG config ###
log_path = pjoin(source_dir, "LOG", f'cleanup_{today}.log')
assert os.path.exists(pjoin(source_dir, "LOG")), os.mkdir(pjoin(source_dir, "LOG"))

log_formatter = "%(asctime)s:%(levelname)s:%(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=log_formatter)
logging.info("Start App ===>")
logging.info(f"Source Directory: {source_dir}")
logging.info(f"Desktop path: {desktop}")



                                                                                                        ### Accessory Functions ###
def mkdirs(sorting_dict={}):
    
    """Create a directory in the desktop for each dictionary key"""
    
    assert type(sorting_dict) == dict, f"input should be dict, current type for {sorting_dict} is {type(sorting_dict)}"

    for dirs in sorting_dict.keys():
            dirs_path = pjoin(desktop, dirs, "")
            if os.path.isdir(dirs_path) == False:
                os.mkdir(dirs_path)
                print(rf"New dir : {dirs_path}")

def ui_verify_sorting(sorting_dict, exceptions=[]):
    
    print(f"\nThe sorting is as follows:")
    for k, v in sorting_dict.items():
        print(f"\n{k} : {v}")
    validation = input("Is this the pattern ?")
    if validation == '':
        return True
    else:
        return False

    
def list_desktop_files_full_path(exception_list=[]):
    """Listing full path of desktop files"""

    assert "desktop" in globals(), "No Desktop configured"
    
    files = []
    for item in os.listdir(desktop):
        item = pjoin(desktop, item)
        if os.path.isfile(item) and item not in exception_list:
            files.append(item)
    return files

def user_output(ordered_files, unordered_files):
    from ctypes import windll
    Win = windll.user32
    
    if unordered_files != []:
        Win.MessageBoxW(0, "The file(s) " + '\n'.join(unordered_files) + " is/are being used", "Not removed from desktop", 1)
    else:
        pass

    if ordered_files == []:
        Win.MessageBoxW(0, "Desktop is already clean", "No Action Taken", 1)
        logging.info("Desktop was already clean")
    else:
        removed_files = str("Clean up of :\n\n" + '\n'.join(ordered_files) + " \n\ncompleted successfully")
        Win.MessageBoxW(0, removed_files, "Removed", 1)   

def file_num_increment(full_fpath):
    """Increment (counter) on duplicate files """
    import re
    
    while os.path.isfile(full_fpath) == True:
        
        fpath, fext = os.path.splitext(full_fpath) #['C:\Users\Desktop\file(1)', '.ext']

        if re.findall("[(]\d+[)]", fpath) != []: #Check if there is (x) in the path.
            for counter in range(1000): #Loop 1000 times
                if fpath.endswith(f"({counter})"): 
                    fpath = replace_last(fpath, f"({counter})", f"({counter+1})") #Replace the last occurence of (counter) in the string.
                    full_fpath = fpath + fext
                    break
                else: #here we pass for cases where (counter) is in the file/folder name itself. We skip them.
                    continue
        else: #If there is no (counter), we create (1)
            counter = 1
            full_fpath = fpath + '(' + str(counter) + ')' + fext

    return full_fpath

def replace_last(source_string, replace_what, replace_with):
    """used to replace the last occurence of something in a string. Used only in file_num_increment()"""
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

                                                                                                          ### Main Function ###
def clean_desktop(src_full_paths=[], sorting_dict={}, exception_list=[]):
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

    for src_full_path in src_full_paths:
        src_full_path_lower = src_full_path.lower()  #Setting src_full_path name to lower case for better comparison
        file_name = basename(src_full_path)
        
        for destination, extensions in sorting_dict.items(): #Looping through input dictionary
            
            assert type(extensions) == list, f"Extensions should be presented in a list [], current value is {extension}"

            dst_dir = pjoin(desktop, destination)
            dst_full_path = pjoin(desktop, destination, file_name)
            
            for ext in extensions: #Looping through the list of extensions
                
                assert type(ext) == str, f"Extensions should be strings, not {ext} that is of type {type(ext)}"
                
                if src_full_path_lower.endswith(ext.lower()):
                    
                    try : 
                            os.rename(src_full_path, dst_full_path)
                            
                            #Adding the file name to the output list and writing log
                            ordered_files.append(file_name)
                            logging.info(f"..\Desktop\{file_name} --> ..\{dst_dir}")

                    except FileExistsError:
                            dst_full_path = file_num_increment(dst_full_path)
    
                            os.rename(src_full_path, dst_full_path)
                            file_new_name = os.path.basename(dst_full_path)

                            #Adding the new file name to the output list and writing log
                            ordered_files.append(file_new_name)
                            logging.info(f"..\Desktop\{file_name} --> ..\{dst_dir}\{file_new_name}")
                            continue

                    except PermissionError: #If the file is in use, user is warned.
                            unordered_files.append(file_name)
                            logging.warning(f"{file_name} not ordered: PermissionError.")
                            
                    except Exception as err:
                            error_msg = f"Error while moving: {file_name}, it was probably not moved"\
                                        f"\n Error:{str(err)}"
                            logging.error(error_msg)

                            



                                                                                                                ### Main ###
logging.info("Start Clean --->")
ordered_files =  []
unordered_files = []
clean_desktop(list_desktop_files_full_path(), file_categories_personal_dict, exception_list=["cleaner.lnk"])
logging.info("---> End Clean")

user_output(ordered_files, unordered_files)
logging.info("===> End App")

"""  ===============> TO DO

Make Subfolder (CodeBase\Scripts)
Reorganize automatically
Not create folders if no files related.

"""

