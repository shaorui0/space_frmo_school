import threading 
import socket
import time
import os
import json
'''
该类实现网络数据传输
可实现多发多收功能 所有的命令接收以后会缓存咋爱commandQueue中 
为每个作战单位提供通信支持
数据协议简单说明 
{
    type:file/command      
    content:filename/datacontent
}

data={'type':file/command ,'content':{fijsd}}

state:Done
'''
"""
class Communication:                    
    serverMainThread=None
    stopFlag=False
    server={'fd':0,'addr':None}
    MAX_BUFFER=4096
    max_client=0
    commandQueue=[]
    threadQueue=[]
    def __init__(self, port:'int>0',maxClient:'int>1'=10,bufferSize:int=4096,fileBaseDir='./source'):
        self.MAX_BUFFER=bufferSize
        self.server['fd'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server['addr']=('localhost', port)
        self.server['fd'].bind(self.server['addr'])
        self.server['fd'].settimeout(5)
        self.max_client=maxClient
        self.lock = threading.Lock()
        self.fileBaseDir=fileBaseDir
        self.serverMainThread=threading.Thread(target=self.mainProcess)
        self.serverMainThread.start()
    def mainProcess(self):
        self.server['fd'].listen(self.max_client)
        print('本机地址:',self.server['addr'])
        while(not self.stopFlag):
            # temp=''
            cfd=[]
            addr=[]
            while(not self.stopFlag and cfd == [] ):
                try:
                    cfd,addr=self.server['fd'].accept()
                except:
                    pass
                    # print('waiting')
                else:
                    pass
            if(cfd==[]):
                continue
                # print('cfd',cfd)
            # print('接收到连接',addr)
            sclient={'fd':cfd,'addr':addr}
            temp=threading.Thread(target=self.clientProcess,args=(sclient,))
            self.threadQueue.append(temp)
            temp.start()
            time.sleep(0.001)
            for i,obj in enumerate(self.threadQueue):
                if(obj.is_alive()==False):
                    del(self.threadQueue[i])
        self.server['fd'].close()
    def clientProcess(self,client):
        buffer=client['fd'].recv(self.MAX_BUFFER)
        tempBuffer=self.deal(buffer,client)
        if(tempBuffer!=None):
            client['fd'].send(tempBuffer)
        client['fd'].close()   
    def deal(self,buffer:bytes,client:dict):
        lens=len(buffer)
        index=0
        for i in range(lens):
            if(buffer[i]==bytes('\n','utf8')[0]):
                index=i
                break
        tempDict=buffer[:index]
        tempDict=tempDict.decode('utf8')
        content=''
        if(index<lens-1):
            content=buffer[index+1:]
        tempDict=eval(tempDict)
        commandDict=None
        if(tempDict['type']=='file'):
            
            fileSize=tempDict['content']['size']
            fileName=os.path.join(self.fileBaseDir,'receive',tempDict['content']['fileName'])

            commandDict={'addr':client['addr'],'type':tempDict['type'],'content':{'fileName':fileName,'size':fileSize}}
            print('get file:',fileName)
            f=open(fileName,'wb')
            lens=len(content)
            index=0
            if(lens>0):
                f.write(content)
                index=lens
            while(index<fileSize):
                if(fileSize-index<self.MAX_BUFFER):
                    bufferT=client['fd'].recv(fileSize-index)
                else:
                    bufferT=client['fd'].recv(self.MAX_BUFFER)
                f.write(bufferT)
                index+=len(bufferT)
                bufferT=[]    
            print('size:',index,'/',fileSize)
        else:
            commandDict={'addr':client['addr'],'type':tempDict['type'],'content':tempDict['content']}
        self.lock.acquire()
        self.commandQueue.append(commandDict)
        self.lock.release()
        return "ok".encode('utf8')


    def sendData(self,addr:tuple,content:dict):
        tempFd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempFd.connect(addr)
        if(content['type']=='command'):
            buffer=json.dumps(content)+'\n'
            bufferT=buffer.encode('utf8')
            tempFd.send(bufferT)
        if(content['type']=='file'):    
            fileName=content['content']['fileName']
            fileSize=os.path.getsize(fileName)
            commandTemp={'type':content['type'],'content':{'fileName':os.path.basename(fileName),'size':fileSize}}
            buffer=json.dumps(commandTemp)+'\n'
            bufferT=buffer.encode('utf8')
            tempFd.send(bufferT)
            time.sleep(0.001)
            f=open(fileName,'rb')
            index=0
            while(index<fileSize):
                buffer=f.read(self.MAX_BUFFER)
                tempFd.send(buffer)
                index+=len(buffer)
            print('send filesize:',index,'/',fileSize)
        tempFd.close()
"""
