# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 01:53:12 2021

@author: ShiningStone
"""
from StellarInfra import Event
from StellarInfra.Event import CEventEngine

def right():
    print('turn right')

if __name__ == '__main__':
    with CEventEngine() as oEngine:
        Event.oCommandDict('right', right)
        oEngine.start()