# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:07:00 2020

@author: Jin Dou
"""
import json
import array,os
import numpy as np
from scipy import io as scipyIO
from .DirManage import checkFolder
from functools import singledispatch


@singledispatch
def toJson(val):
    """ default for json"""
    return val

@toJson.register(np.float32)
def toJson_float32(val):
    """ for np float 32"""
    return np.float64(val)

''' Python Object IO'''
def saveObject(Object,folderName,tag, ext = '.bin'):
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
''' End '''

'''load Matlab .Mat file '''

def loadMatFile(matFilePath):
    return scipyIO.loadmat(matFilePath)

def saveMatFile(matFilePath,mdict,**kwargs):
    return scipyIO.savemat(matFilePath,mdict,**kwargs)
''' End '''