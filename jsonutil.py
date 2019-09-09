import os

def remove(path):

    files = []
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files: 
            curPath = path + "/" + file
            if os.path.isdir(curPath) and (file != "vott-json-export"):
                remove(curPath) 
            elif os.path.isfile(curPath) and (file != "test.vott"):
                os.remove(curPath)


def dict2obj(obj,dict):
    obj.__dict__.update(dict)
    return obj

    
