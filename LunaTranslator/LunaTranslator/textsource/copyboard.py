 
import time  
from textsource.textsourcebase import basetext
from utils.config import globalconfig
import winsharedutils,ctypes,win32utils,os
class copyboard(basetext):
    def __init__(self,textgetmethod) -> None:
        self.last_paste_str = '' 
          
        super(copyboard,self).__init__(textgetmethod,'0','0_copy')
    
    def gettextthread(self ):
                 
            time.sleep(0.1)
            paste_str = winsharedutils.clipboard_get()
            
            if self.last_paste_str != paste_str:
                self.last_paste_str =paste_str 
                if globalconfig['excule_from_self']   and win32utils.GetWindowThreadProcessId(win32utils.GetClipboardOwner())==os.getpid():
                    return  
                return (paste_str)
    def runonce(self): 
        self.textgetmethod(winsharedutils.clipboard_get(),False)