import json
import os
from random import shuffle


pjoin = os.path.join
cwd = os.getcwd

if not os.path.isdir(pjoin(cwd(), "DummyDesktop")):
    os.mkdir("DummyDesktop")

os.chdir("DummyDesktop")

def get_shuffled_extensions():
    from file_extensions_general import file_categories
    extensions = []
    for v in file_categories.values():
        extensions = extensions + [x.lower() for x in v] + [x.lower() for x in v]
    shuffle(extensions)
    return extensions

def get_shuffled_names(): 
    path = r"C:\Users\NG8203C\Desktop\English Dictionary JSON"
    dictionary_files = os.listdir(path)

    names = []
    for file in dictionary_files :
        with open(os.path.join(path, file), encoding='utf-8') as f:
            dictionary = json.loads(f.read())
        words = [word for word in dictionary.keys()]
        long_words = [word for word in words if len(word) >= 20]
        names += long_words
    shuffle(names)
    return names
                
def create_dummy_filenames():
    global dummy_files
    dummy_files = []
    for base_filename, extension in zip(get_shuffled_names(), get_shuffled_extensions()):
        dummy_files.append(pjoin(cwd(), base_filename + extension))

    for file in dummy_files:
        open(file, 'a').close()
        

if __name__ == "__main__":
    create_dummy_filenames()

