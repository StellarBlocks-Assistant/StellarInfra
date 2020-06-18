# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:13:44 2020

@author: Jin Dou
"""

import StellarInfra.DirManage as DIR
from StellarInfra.Logger import CLog
import array

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

StageControl.stageList = [1,3,4]
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

oStage = CStageControl([1,3,4])

if oStage(1):
    print(1)
    
if oStage(2):
    print(2)
    
if oStage(4):
    print(4)
    
    
