# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:37:03 2020

@author: Jin Dou
"""
import datetime
from .DirManage import checkFolder
#maybe considering the offcial logging lib in the future

LOG_MODE = ['safe','fast']
PRINT_MODE = [True,False]
LOG_MODE = [True,False]
import sys
class CLog:
  
    def __init__(self,folder=None,Name=None):
        self._mode = 'safe' # 'fast' | 'safe'
        self._printFlag = True
        self._logFlag = True
        self._buffer = list()
        self.folder = None
        self.name = None
        self.fileName = None
        if folder != None and Name != None:
            checkFolder(folder)
            self.fileName = folder+Name + '.txt'
            self.Open()
            self.Save()
            self.folder = folder
            self.name = Name
        else:
            self.fileHandle = None
    
    @property
    def Mode(self):
        return self._mode
    
    @Mode.setter
    def Mode(self,value):
        if value not in LOG_MODE:
            raise ValueError('value of mode is wrong ',LOG_MODE)
        else:
            self._mode = value
            
    @property
    def ifPrint(self):
        return self._printFlag
    
    @ifPrint.setter
    def ifPrint(self,value):
        if value not in PRINT_MODE:
            raise ValueError('value of mode is wrong ',PRINT_MODE)
        else:
            self._printFlag = value
            
    @property
    def ifLog(self):
        return self._logFlag
    
    @ifLog.setter
    def ifLog(self,value):
        if value not in LOG_MODE:
            raise ValueError('value of mode is wrong ',PRINT_MODE)
        else:
            self._logFlag = value
    
    @property
    def usable(self):
        if(self.fileHandle != None):
            return True
        else:
            return False
    
    def Open(self):
        if not self.usable:
            return False
        self.fileHandle = open(self.fileName, "a+")
        
    def Save(self):
        if not self.usable:
            return False
        self.fileHandle.close()
        
    def Write(self,Str):
        if self._printFlag:
            sys.stdout.write(Str)
        if not self.usable:
            return False
        if self.ifLog:
            if self._mode == 'safe':
                self.Open()
                self.fileHandle.write(Str)
                self.Save()
            else:
                self._buffer.append(Str)
        
    def record(self,*logs,splitChar=' ',newline:bool = True):
        for idx,log in enumerate(logs):
            Str = str(log)
            if idx != len(logs) - 1 :
                self.Write(Str + splitChar)
            else:
                self.Write(Str)
        
        if(newline == True):
            self.Write('\n')
        else:
            self.Write(splitChar)
        
    def safeRecord(self,*logs,splitChar=' ',newline:bool = True):
        temp = self._mode
        self.Mode = 'safe'
        self.record(*logs,splitChar=splitChar,newline = newline)
        self.Mode = temp
    
    def safeRecordTime(self,*logs,splitChar=' ',newline:bool = True):
        now = datetime.datetime.now()
        self.safeRecord(*logs,now,splitChar=splitChar ,newline = newline)
        
    def saveBuffer(self):
        if not self.usable:
            return False
        for log in self._buffer:
            self.fileHandle.write(log)
        self.Save()
        
    def __call__(self,*logs,splitChar=' ',newline:bool = True):
        return self.record(*logs,splitChar = splitChar, newline = newline)
    
    def t(self,*logs,splitChar=' ',newline:bool = True):
        now = datetime.datetime.now()
        return self.record(*logs,now,splitChar=splitChar ,newline = newline)
        
    def __del__(self):
        if(len(self._buffer) > 0):
            self.saveBuffer()
        self.Save()
    