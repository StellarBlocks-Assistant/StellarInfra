# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:07:00 2020

@author: Jin Dou
"""
import json
import array,os
import numpy as np
from scipy import io as scipyIO
from .DirManage import checkFolder, checkExists
from functools import singledispatch
import pandas as pd

class OSMeta(type):
    
    def __init__(cls, *args, **kwargs):
         pass
         
    @property
    def win(cls):
        name = os.name
        if name == 'nt':
            return True
        else:
            return False
     
    @property
    def unix(cls):
        name = os.name
        if name == 'posix':
            return True
        else:
            return False


class OS(metaclass=OSMeta):
    pass
    

@singledispatch
def toJson(val):
    """ default for json"""
    # print(val,type(val))
    if isinstance(val, np.ndarray):
        return val.tolist()
    else:
        return val

@toJson.register(np.ndarray)
def toJson_npArray(val):
    # print('!!!')
    return val.tolist()

@toJson.register(np.int64)
def toJson_int(val):
    """ for np float 32"""
    return int(val)

@toJson.register(np.float32)
def toJson_float32(val):
    """ for np float 32"""
    return np.float64(val)

''' Python Object IO'''
def saveObject(Object,folderName,tag=None, ext = '.bin'):
    if tag is None:
        file = open(folderName, 'wb')
    else:
        checkFolder(folderName)
        file = open(folderName + '/' + str(tag) + ext, 'wb')
    import pickle
    pickle.dump(Object,file)
    file.close()
    
def loadObject(filePath):
    import pickle
    file = open(filePath, 'rb')
    temp = pickle.load(file)
    return temp

def saveDictJson(filePath:str,Obj:dict):
    with open(filePath,'w') as file:
        json.dump(Obj,file,default = toJson,indent=4)
        
def loadJson(filePath:str):
    out = None
    with open(filePath) as json_file:
        out = json.load(json_file)
    return out
''' End '''

''' Load Bin and Text File '''
def loadBinFast(Dir,Type:str = 'd'):
    f = open(Dir,'rb')
    a = array.array(Type)
    a.fromfile(f, os.path.getsize(Dir) // a.itemsize)
    return np.asarray(a)
    
def loadText(path):
    f=open(path, "r")
    contents = f.read()
    f.close()
    return contents

def loadTextLines(path):
    f=open(path, "r")
    contents = f.readlines()
    f.close()
    return contents

def loadCSV(path):
    df = pd.read_csv(path)
    out = {}
    for i in df:
        out[i] = df[i].tolist()
    return out

''' End '''

'''load Matlab .Mat file '''

def loadMatFile(matFilePath):
    try:
        return scipyIO.loadmat(matFilePath)
    except:
        import mat73
        return mat73.loadmat(matFilePath)

def saveMatFile(matFilePath,mdict,**kwargs):
    return scipyIO.savemat(matFilePath,mdict,**kwargs)
''' End '''


''' A mixin class for generate and load data usage'''
#Mode:
class Enum:
    READ = 'read'
    WRITE = 'write'

class MixinDataInOut:
    
    def __init__(self,path):
        if checkExists(path):
            self._mode = Enum.READ
        