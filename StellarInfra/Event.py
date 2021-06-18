# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 01:23:02 2021

@author: ShiningStone
"""

import socket,select
from multiprocessing.connection import Listener
from multiprocessing.managers import BaseManager  
import multiprocessing as mp
from multiprocessing.connection import Client

class ReturnCode:
    WARNING_NOTHING_TO_RECV = -1

class CCommandDict:
    
    def __init__(self):
        self.command = dict()

    def __call__(self,key,func):
        if(callable(func)):
            self.command[key] = func
        else:
            raise ValueError("input should be a function")
            
    def __getitem__(self,key):
        return self.command[key]
    
def left():
    print('turn left')
oCommandDict = CCommandDict()
oCommandDict('left',left)


class CServer:
    
    def __init__(self,address:tuple):
        self.address = address
        self.listener = Listener(self.address, authkey=b'secret password')
        self.conn = None
        
    def start(self):
        print('waiting for connection')
        self.conn = self.listener.accept()
    
    def recv(self):
        return self.conn.recv()
    
    def send(self,content):
        return self.conn.send(content)
    
    def close(self):
        return self.conn.close()
    
    def poll(self,timeout=1):
        return self.conn.poll(timeout=timeout)
    
    def getConnection(self):
        return self.conn
    
class CCrsProcManager(BaseManager):
    pass

CCrsProcManager.register('server', CServer)#regested class in Manager can only use the class's method but not attribute
#https://docs.python.org/3.6/library/multiprocessing.html#multiprocessing.managers.BaseManager.register

def onCallRecvDaemon(address,oServer:CServer,oRecvCache:mp.Queue):
    oSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    oSocket.bind(address)
    oSocket.listen()
    oInnerConn,addr = oSocket.accept()
    print('onCallRecv: connected')
    oOuterConn = oServer.getConnection()
    readList = [oSocket,oOuterConn,oInnerConn]
    while True:
        rd,wt,ex = select.select(readList,[],[])
        for r in rd:
            if r is oSocket:
                c,addr = r.accept()
                oInnerConn = c
                readList.append(c)
                print('onCallRecv: connected')
            elif r is oOuterConn:
                if r.poll(3):
                    try:
                        recvMsg = oOuterConn.recv()
                    except:
                        recvMsg = ''
                        print('onCallRecv: the other side is closed')
                        readList.remove(oOuterConn)
                    else:
                        print('onCallRecv_recv_msg: ',recvMsg)
                        oRecvCache.put(recvMsg)
                        oInnerConn.send(b'newMsg')
                        if(recvMsg == 'quitBusyMode'):
                            return
            elif r is oInnerConn:
                data = r.recv(512)
                msg = data.decode()
                print('onCallRecv_recv_instr:',msg)
                if(msg == 'close'):
                    oSocket.close()
                    return
    return
    

def onCallSendDaemon(address,oServer:CServer,oSendCache:mp.Queue):
    oSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    oSocket.bind(address)
    oSocket.listen()
    oInnerConn,addr = oSocket.accept()
    print('onCallSend_connected')
    oOuterConn = oServer.getConnection()
    readList = [oSocket,oInnerConn]
    while True:
        rd,wt,ex = select.select(readList,[],[])
        for r in rd:
            if r is oSocket:
                c,addr = r.accept()
                oInnerConn = c
                readList.append(c)
                print('onCallSend_connected')
            elif r is oInnerConn:
                data = r.recv(512)
                msg = data.decode()
                print('onCallSend_recv_instr:',msg)
                if('send' in msg): #close and send can be concatenated together
                    while (not oSendCache.empty()):
                        try:
                            sendMsg = oSendCache.get(timeout = 3)
                        except:
                            sendMsg = ''
                        else:
                            oOuterConn.send(sendMsg)
                            print('onCallSend_send_msg: ', sendMsg)
                if('close' in msg):
                    oSocket.close()
                    return


class CEventEngine:
    def __init__(self):
        self.address = ('localhost', 6085)
        self.addressSendDaemon = ('localhost',8300)
        self.addressRecvDaemon = ('localhost',8301)
        self.oCrsProcManager = CCrsProcManager()
        self.oServer = None
        self.oRecvCache = mp.Queue()
        self.oSendCache = mp.Queue()
        self.prcRecv = None
        self.prcSend = None
        global oCommandDict
        self.oCommandDict = oCommandDict
        
    def __enter__(self):
        return self
    
    def __exit__(self,*args,**kwargs):
        self._close()
        

    def start(self):
        print('start server ...')
        self.oCrsProcManager.start()
        self.oServer = self.oCrsProcManager.server(self.address)
        self.oServer.start()
        print('server start')
        self.prcRecv = mp.Process(target = onCallRecvDaemon, 
                                  args=[self.addressRecvDaemon,self.oServer, self.oRecvCache])
        
        self.prcSend = mp.Process(target = onCallSendDaemon,
                                  args=[self.addressSendDaemon,self.oServer, self.oSendCache])
        
        while (True):
            recvMsg = self.oServer.recv()
            if(recvMsg == 'busyMode'):
                err = self.busyMode()
                if(err == 0):
                    break
            elif(recvMsg == 'close'):
                break
            elif(recvMsg in self.oCommandDict.command.keys()):
                    print('start handling service request: ' + recvMsg)
                    self.handleRegisteredService(recvMsg)
                    print('finish handling service request: ' + recvMsg)
            else:
                print('recv msg: ',recvMsg)
            
        self.handleCloseMsg()
        return 0
    
    def busyMode(self):
        print('enter busy mode')
            
        self.prcRecv.start()
        self.prcSend.start()
        
        self.oSockSendDaemon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.oSockRecvDaemon = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.oSockSendDaemon.connect(self.addressSendDaemon)
        self.oSockRecvDaemon.connect(self.addressRecvDaemon)
        readList = [self.oSockRecvDaemon]
        timeout = 5
        print('main server select timeout:',timeout)
        while True:
            rd,wt,ex = select.select(readList,[],[],timeout)
            for r in rd:
                if r is self.oSockRecvDaemon:
                    data = r.recv(512)
                    msg = data.decode()
                    print('main server recv inner msg:', msg)
                    if(msg == 'newMsg'):
                        while not self.oRecvCache.empty():
                            recvMsg = ''
                            try:
                                recvMsg = self.oRecvCache.get(timeout=1)
                            except:
                                recvMsg = ''
                            print('main server recv msg:', recvMsg)
                            if(recvMsg == 'close'):
                                self.closeBusyMode()
                                return 0
                            elif(recvMsg in self.oCommandDict.command.keys()):
                                print('start handling service request: ' + recvMsg)
                                self.handleRegisteredService_busyMode(recvMsg)
                                print('finish handling service request: ' + recvMsg)
                            elif(recvMsg == 'quitBusyMode'):
                                self.closeBusyMode()
                                return 1
                            else:
                                print("receive unhandled msg: ",recvMsg)
                    
        return 0
    
    def handleRegisteredService(self,key):
        result= ''
        result = self.oCommandDict[key]()
        self.oServer.send(key)
        print('send_msg: ',key)
    
    def handleRegisteredService_busyMode(self,key):
        result= ''
        result = self.oCommandDict[key]()
        self.oSendCache.put(key)
        self.oSockSendDaemon.send(b'send')
    
    def closeBusyMode(self):
        self.oSockSendDaemon.send(b'send')
        err1 = self.oSockSendDaemon.send(b'close')
        err2 = self.oSockRecvDaemon.send(b'close')
        #        self.oSendCache.put('All is closed')
        err1 = self.prcSend.join()
        print('prcSend join return',err1)
            
        err2 = self.prcRecv.join() #it seems that if join() wait for too long, it will block forever; Maybe because the deadlock between existed recv process and the queue cache the recv process keeps
        print('prcRecv join return',err2)

        print('quit busy mode')
        return "CKnowledgeServer_busyMode_close"
    
    def handleCloseMsg(self):
        self.oServer.send('All is closed')
        print('send_msg: All is closed')
        self._close()
        return "CKnowledgeServer_close"
    
    def _close(self):
        try:
            try:
                self.prcRecv.close()
            except:
                self.prcRecv.terminate()
            try:
                self.prcSend.close()
            except:
                self.prcSend.terminate()
        except:
            pass
        self.oRecvCache.close()
        self.oSendCache.close()
        # self.oServer.close()
        self.oCrsProcManager.shutdown()
        print('server_close')
        print('----------------------------------------')
            
class CEventClient:
    
    def __init__(self,addressTuple,authkey=b'secret password',oLog = None):
        self.addressTuple = addressTuple
        self.authkey = authkey
        self.conn = None
        self.oLog = oLog
        
    def connect(self):
        try:
            self.conn = Client(self.addressTuple, authkey=self.authkey)
        except:
            self.modMsg('connection is refused')
            return False
        else:
            return True
    
    def send(self,msg):
        if(not self.closedFlag):
            return self.conn.send(msg)
        else:
            self.modMsg('connection is closed')
            return False
        
    def recv(self,block = False):
        if(not self.closedFlag):
            if block:
                return self.conn.recv()
            if(self.conn.poll()):
                return self.conn.recv()
            else:
                return ReturnCode.WARNING_NOTHING_TO_RECV
        else:
            self.modMsg('connection is closed')
            return False
    
    def close(self):
        if(not self.closedFlag):
            self.conn.send('close')
            try:
                msg = self.conn.recv()
                print(msg)
                if(msg == 'All is closed'):
                    self.conn.close()
                    return True
                else:
                    return False
            except:
                self.modMsg('nothing to recv')
                return False
        else:
            self.modMsg('connection is closed')
            return False
            
    def modMsg(self,string:str):
        string = self.__class__.__name__ + ' warning: ' + string
        if(self.oLog != None):
            self.oLog.safeRecordTime(string)
        else:
            print(string)
    
    @property        
    def closedFlag(self):
        if(self.conn == None ):
            return True
        else:
            return self.conn.closed