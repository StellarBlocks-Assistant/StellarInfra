# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 01:49:13 2021

@author: ShiningStone
"""

from StellarInfra.Event import CEventClient
import keyboard
import sys

oClient = CEventClient(('192.168.1.111', 6085))
assert oClient.connect()
def onAPressed():
    oClient.send('a')
    recvMsg = oClient.recv()
    print("receive: ", recvMsg)
    # print('a')
    
def onDPressed():
    # print('d')
    oClient.send('d')
    recvMsg = oClient.recv()
    print("receive: ", recvMsg)
    
def onQPressed():
    print('q')
    oClient.close()
    keyboard.press_and_release('ctrl+c')

keyboard.add_hotkey('a', onAPressed)
keyboard.add_hotkey('d', onDPressed)
keyboard.add_hotkey('q', onQPressed)
keyboard.wait()
# assert oClient.connect()
# while True:
#     key = keyboard.read_hotkey()
#     if key == 'a':
#         oClient.send('a')
#         recvMsg = oClient.recv()
#         print("receive: ", recvMsg)
#     elif key == 'd':
#         oClient.send('d')
#         recvMsg = oClient.recv()
#         print("receive: ", recvMsg)
    # value = input("Please enter a command:\n")
    # if value.lower() != 'close':
    #     oClient.send(value)
    #     recvMsg = oClient.recv()
    #     print("receive: ", recvMsg)
    # else:
    #     recvMsg = oClient.close()
    #     print("receive: ", recvMsg)
    #     break
    
    