# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 01:49:13 2021

@author: ShiningStone
"""

from StellarInfra.Event import CEventClient

oClient = CEventClient(('localhost', 6085))
oClient.connect()
while True:
    value = input("Please enter a command:\n")
    if value.lower() != 'close':
        oClient.send(value)
        recvMsg = oClient.recv()
        print("receive: ", recvMsg)
    else:
        recvMsg = oClient.close()
        print("receive: ", recvMsg)
        break
    
    