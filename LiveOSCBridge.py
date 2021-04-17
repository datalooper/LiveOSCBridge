import Live
from _Framework.ControlSurface import ControlSurface

from .OSCHelper import OSCHelper
import threading

class LiveOSCBridge(ControlSurface):
    
    def __init__(self, c_instance):
        super(LiveOSCBridge, self).__init__(c_instance)
        self.__c_instance = c_instance
        with self.component_guard():
            self.OSCHelper = OSCHelper('127.0.0.1', 9001, 0, self.log_message)
            self.OSCHelper.setOSCHandler('default', self.default)

    def disconnect(self):
        self.OSCHelper.disconnect()
        
    def default(self, addr, tags, data,source):
    # Handle all OSC messages in default handler
        self.log_message("default")
        # self.song().tempo = self.song().tempo + 5


    



