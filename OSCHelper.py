from .OSC3 import OSCServer, ThreadingOSCServer, ForkingOSCServer, OSCClient, OSCMessage, OSCBundle
import threading


class OSCHelper():
    server = 0
    client = 0
    st = 0

    def __init__(self, ip, port, server_type, log_message):
        self.log_message = log_message
        self.initOSCServer(ip, port, server_type)  
        self.startOSCServer() # and now set it into action

    def printing_handler(self,addr, tags, data, source):
        self.log_message("---")
        self.log_message( "received new osc msg from %s" % getUrlStr(source))
        self.log_message( "with addr : %s" % addr)
        self.log_message( "typetags :%s" % tags)
        self.log_message( "the actual data is : %s" % data)
        self.log_message( "---")

    def initOSCClient(self,ip='127.0.0.1', port=9001) :
        self.client = OSCClient()
        self.client.connect( (ip,port) )
        
    def initOSCServer(self,ip='127.0.0.1', port=9000, mode=0) :
        # """ mode 0 for basic server, 1 for threading server, 2 for forking server
        # """
        if mode == 0 :
            self.server = OSCServer( (ip ,port) ) # basic
        elif mode == 1 : 
            self.server = ThreadingOSCServer( (ip ,port) ) # threading
        elif mode == 2 :
            self.server = ForkingOSCServer( (ip ,port) ) # forking        
    def disconnect(self) :
        if self.client is not 0 : self.client.close()
        if self.server is not 0: self.server.close() 
        if self.st is not 0: self.st.join()

    def startOSCServer(self) :
        self.st = threading.Thread( target = self.server.serve_forever )
        self.st.start()
        self.server.addDefaultHandlers()
        self.log_message( "Registered Callback-functions are :")
        for addr in self.server.getOSCAddressSpace():
            self.log_message( str(addr))

    def setOSCHandler(self,address, hd) :
        self.server.addMsgHandler(address, hd) # adding our function

    def closeOSC(self) :
        if self.client is not 0 : self.client.close()
        if self.server is not 0: self.server.close() 
        if self.st is not 0: self.st.join()

    def reportOSCHandlers(self) :
        self.log_message( "Registered Callback-functions are :")
        for addr in self.server.getOSCAddressSpace():
            self.log_message( str(addr))
        
    def sendOSCMsg( self,address='/print', data=[] ) :
        m = OSCMessage()
        m.setAddress(address)
        for d in data :
            m.append(d)
        self.client.send(m)

    def createOSCBundle(self,address) :
        return OSCBundle(address)
        
    def sendOSCBundle(self,b):
        self.client.send(b)

    def createOSCMsg(self,address='/print', data=[]) :
        m = OSCMessage()
        m.setAddress(address)
        for d in data :
            m.append(d)
        return m