import PySimpleGUI as sg
from os import path
from mapping import available_maps


EXCEPTION_LIST = []
click = 0

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'

def generate_mapping_frame(_map:dict):
    """This builds a kind of pysimplegui "frame list"/table for the provided map"""
    Title = _map.name
    Labels = []
    Listboxes = []
    InputText = []
    OKs = []
    for k, values in _map:
        label = sg.Text(k, size = (9, 1))
        li = sg.Listbox(values=values, key=f"{Title}_{k}_list", size=(10, 10), no_scrollbar=True, enable_events=True)
        _in = sg.InputText('.txt', key=f"{Title}_{k}", size=(9,1))
        ok = sg.OK('Add', key=f"add_{Title}_{k}", visible=False)
        Labels.append(label)
        Listboxes.append(li)
        InputText.append(_in)
        OKs.append(ok)
        
    return sg.Frame(Title, [Labels, Listboxes, InputText, OKs])

layout = [[sg.Text('Folder to order')],
          [sg.InputText(key='base_dir', size=(60,1)), sg.FolderBrowse()],
          [sg.Text('                         ', auto_size_text=True, key="INFO", visible = False)],
          [sg.OK(key='select_dir'), sg.Cancel()],
          [generate_mapping_frame(available_maps[0])],
          [generate_mapping_frame(available_maps[1])],
          [sg.Text('Exceptions')],
          [sg.Listbox(values=EXCEPTION_LIST, key='exceptions_list', size=(10, 10), no_scrollbar=True, enable_events=True)],
          [sg.InputText('.txt', key='exception',size=(10,1)), sg.OK('Add', key="add_exception", visible=False)],
          ]


window = sg.Window('Orderer', layout, return_keyboard_events=True)

associated_fields = {       #This is to handle when user presses Enter on a text field
    'base_dir' : window.Elem('select_dir'),
    'exception' : window.Elem('add_exception'),
                     }


while True:
    event, inputs = window.Read()
    if len(event) > 1:
        print(event, inputs)
    
    if event is None:
        break
#---------- Presing Enter------------
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):       # Check for ENTER key
        elem = window.FindElementWithFocus()                            # go find element with Focus
        if elem.Type == sg.ELEM_TYPE_INPUT_TEXT: #if its a text field, click on the associated button
            if elem.Key in list(associated_fields.keys()):
                elem = associated_fields[elem.Key]
        if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:       # if it's a button element, click it
            elem.Click()

#---------- Selecting Dir------------            
    if event == "select_dir":
        if inputs['base_dir'] != '':
            if path.isdir(inputs['base_dir']):
                window.Element('INFO').Update(visible=False)
                desktop = inputs['-IN-']
                event = 'Exit'                
            else:
                window.Element('INFO').Update("Not a valid folder name")
                window.Element('INFO').Update(visible=True)

#---------- Mapping ------------ 
    def handle_lists_change(event, inputs):
        pass
#---------- Adding Elements------------ 
    if event == "add_exception":
        if inputs['exception'] != '':
            exception = inputs['exception']
            EXCEPTION_LIST.append(exception)
            window.Element('exceptions_list').Update(values=EXCEPTION_LIST)
            window.Element('exception').Update('')
            
    
#---------- Removing Elements------------
    if event == "exceptions_list" and click < 1:
        click += 1
        continue
    if event == "exceptions_list" and click >= 1 and EXCEPTION_LIST != list():
        EXCEPTION_LIST.remove(window.Element('exceptions_list').get()[0])
        window.Element('exceptions_list').Update(values=EXCEPTION_LIST)
        click = 0

    if event in (None, 'Exit'):      
        break  
window.Close()




