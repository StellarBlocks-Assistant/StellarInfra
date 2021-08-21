# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:13:44 2020

@author: Jin Dou
"""

import StellarInfra.DirManage as DIR
from StellarInfra.Logger import CLog
import array
from StellarInfra.DirManage import CDirectoryConfig

DIR.checkFolder('test/')
DIR.getFileList('test/','txt')
DIR.getFileName('test/jin.txt')
DIR.getSubFolderName('./')

bufR = array.array('B',(0,)*352*288)
with open('test/test.bin','wb') as f:
    bufR.tofile(f)
    
import StellarInfra.IO as IO

a = IO.loadBinFast('test/test.bin','B')

class TestObj:
    def __init__(self):
        pass
    
IO.saveObject(TestObj,'./test/','testObj')
b = IO.loadObject('./test/testObj.bin')

from StellarInfra import StageControl

StageControl.stageList = [5]
from StellarInfra.StageControl import decorStage,CStageControl
@decorStage(1)
def func1():
    print('1')

@decorStage(2) 
def func2():
    print('2')

@decorStage(3) 
def func3():
    print('3')
    
func1()
func2()
func3()

oStage = CStageControl([6])

if oStage(1):
    print(1)
    
if oStage(2):
    print(2)
    
if oStage(4):
    oLog1 = CLog('./Test/','test')
    oLog2 = CLog('./Test/','test','.bak')
    print(4)
    oLog1.t(1,2,3)
    oLog1.t(5,6,7,splitChar='\t')
    oLog1.t(8,9,10,splitChar = ',',newline = False)
    oLog1.t(11,12,13,newline = True)
    import time
    oLog2.Mode = 'fast'
    for i in range(5):
        time.sleep(1)
        oLog2(1,2,3)
    oLog2.Mode = 'safe'
    print(oLog2._mode)
    oLog2(4,5,6)
    oLog2.Mode = False
    oLog2(7,8,9)
    oLog2.ifPrint = False
    oLog2(10,11,12)
    oLog2.Mode = 'safe'
    oLog2(13,14,15)
    
if oStage(5):
    oLog = CLog('./Test/','test5')
    oLog.safeRecord('aaaa')
    oLog.Mode = False
    oLog.safeRecord('bbbb')

#oDir = CDirectoryConfig(['Root','Train','Test','MiddleStage','Output','Models'],'Dataset.conf')
if oStage(6):
    from StellarInfra.DirManage import CPathConfig
    oPath = CPathConfig('Stages.conf',checkFolders=False)
    oPath1 = CPathConfig('Stages.yml')
#    oPath2 = CPathConfig('Stages.yaml')
    
    
#Folders: !Folders
#    a: D:\Appendix\Test\TestSTDMYaml