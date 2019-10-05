from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def get_text(file):
    text_clean = ""
    global text_list
    text_list = []
    
    with open(file) as f:
        text_raw = str(f.readlines())
        
    soup = BeautifulSoup(text_raw, features="lxml")
    
    # get text 
    text_clean = soup.get_text("\n", strip=True)
    #convert to list
    text_list = list(text_clean.split("\n"))
    
    print(text_clean, "return type is list")
    return text_list
    



Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

get_text(filename)
