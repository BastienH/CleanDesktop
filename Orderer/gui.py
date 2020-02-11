import PySimpleGUI as sg
from os import path

layout = [[sg.Text('Folder to order')],
              [sg.In(key='-IN-', size=(60,1)), sg.FolderBrowse()],
              [sg.Text('                         ', auto_size_text=True, key="INFO")],
              [sg.OK(key='OK'), sg.Cancel()]]

window = sg.Window('Clean Desktop', layout)

while True:      
    event, values = window.Read() 
    if event == "OK":
        if values['-IN-'] != '':
            if path.isdir(values['-IN-']):
                window.Element('INFO').Update("                    ")
                desktop = values['-IN-']
                event = 'Exit'                
            else:
                window.Element('INFO').Update("Not a valid folder name")
             
    if event in (None, 'Exit'):      
        break      

window.Close()


