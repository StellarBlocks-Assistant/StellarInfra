# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:11:13 2020

@author: Jin Dou
"""

import os
import warnings
from configparser import ConfigParser,BasicInterpolation

def getUpperDir(path:str):
    return os.path.split(path)

def isFolderOrFile(path:str):
    '''
    not exist 0
    dir 1
    file 2
    others -1
    '''
    out = -1
    if checkExists(path):
        if os.path.isdir(path):
            out = 1
        elif os.path.isfile(path):
            out = 2
    else:
        out = 0
    return out

def checkExists(path):
    return os.path.exists(path)

def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        warnings.warn("path: " + folderPath + " doesn't exist, and it is created")
        os.makedirs(folderPath)

def getFileList(folder_path,extension):
    ans = [os.path.join(folder_path,file) for file in os.listdir(folder_path) if file.endswith(extension)]
    if(len(ans)==0):
        warnings.warn("getFileList's error: folder: '" + str(folder_path) + "'is empty with '" + str(extension) + "' kind of file")
        return None
    else:
        return ans
    
def getFileName(path):
    dataSetName, extension = os.path.splitext(os.path.basename(path))    
    return dataSetName,extension

def getSubFolderName(folder):
    subfolders = [f.name for f in os.scandir(folder) if f.is_dir() ]
    return subfolders

class DummyObj:
    pass

class CDirectoryConfig:
    
    def __init__(self,dir_List, confFile):
        self._dir_dict = dict()
        self._confFile = confFile
        for i in dir_List:
            self._dir_dict[i] = ''
        self._load_conf()
        self._addAttr()
        self._checkFolders()
            
    def _load_conf(self):
        conf_file = self._confFile
        config = ConfigParser(interpolation=BasicInterpolation())
        config.read(conf_file,encoding = 'utf-8')
        conf_name, ext = getFileName(conf_file)
        for dir_1 in self._dir_dict:
            self._dir_dict[dir_1] = config.get(conf_name, dir_1)
#            print(dir_1,config.get(conf_name, dir_1))
    
    def __getitem__(self,keyName):
        return self._dir_dict[keyName]
    
    def _checkFolders(self,foldersList = None):
        if foldersList != None:
            pass
        else:
            foldersList = self._dir_dict.keys()
        
        for folder in foldersList:
                checkFolder(self._dir_dict[folder])
    
    def _addAttr(self):
        for name in self._dir_dict:
            setattr(CDirectoryConfig,name,self._dir_dict[name])
            
class CPathConfig:
    
    def __init__(self,confFile,sectionList:list = None):
        self._dict = dict()
        self._confFile = confFile
        self._load_conf()
        self._addAttr()
        self._checkFolders()
            
    def _load_conf(self):
        conf_file = self._confFile
        config = ConfigParser(interpolation=BasicInterpolation())
        config.optionxform = str #disable the default changing to lowercase
        config.read(conf_file,encoding = 'utf-8')
        sections = config.sections()
        for sec in sections:
            self._dict[sec] = dict()
        for sec in sections:
            for item in config[sec]:
                self._dict[sec][item] = config.get(sec,item)
                # print(config.get(sec,item))
    
    def __getitem__(self,keyName):
        return self._dict[keyName[0]][keyName[1]]
    
    def _checkFolders(self):

        for sec in self._dict:
            foldersList = self._dict[sec].keys()
            for folder in foldersList:
                path = self._dict[sec][folder]
                _,ext = getFileName(path)
                flag = isFolderOrFile(path)
                if flag == 1:
                    checkFolder(path)
                elif flag == 0:
                    if ext == '':
                        checkFolder(path)
                    else:
                        folder,ext = getUpperDir(path)
                        checkFolder(folder)
                else:
                    assert flag != -1
    
    def _addAttr(self):
        for sec in self._dict:
            setattr(CPathConfig,sec,DummyObj())
            for item in self._dict[sec]:
                setattr(getattr(CPathConfig, sec),item,self._dict[sec][item])
