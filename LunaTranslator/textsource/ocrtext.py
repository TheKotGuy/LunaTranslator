 
import time
from traceback import print_exc 

from utils.config import globalconfig 
import win32file,win32pipe,win32con
import os
import importlib  
from difflib import SequenceMatcher 
import time  
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QPoint
from textsource.textsourcebase import basetext 
from utils.getpidlist import getmagpiehwnd
def compareImage(  imageA :QImage, imageB):
    h,w=imageA.height(),imageA.width()
    sample =sum([sum([ imageA.pixel(i*w//128,j*h//16)==imageB.pixel(i*w//128,j*h//16) for i in range(128)]) for j in range(16)]  )
    return sample/(128*16)
def getEqualRate(  str1, str2):
    
        score = SequenceMatcher(None, str1, str2).quick_ratio()
        score = score 

        return score
import win32gui ,math,win32process
class ocrtext(basetext):
    
    def imageCut(self,x1,y1,x2,y2):
     
        if self.hwnd:
            try:
                _hwnd_magpie=getmagpiehwnd(self.object.translation_ui.callmagpie.pid)
                if _hwnd_magpie!=0:

                    hwnduse=QApplication.desktop().winId()
                else:
                    hwnduse=self.hwnd
                rect=win32gui.GetWindowRect(hwnduse)  
                rect2=win32gui.GetClientRect(hwnduse)
                windowOffset = math.floor(((rect[2]-rect[0])-rect2[2])/2)
                h= ((rect[3]-rect[1])-rect2[3]) - windowOffset
                # print(h)
                # print(rect)
                # print(rect2)
                # print(x1-rect[0], y1-rect[1]-h, x2-x1, y2-y1)
 
                 
                pix = self.screen.grabWindow(hwnduse, x1-rect[0], y1-rect[1]-h, x2-x1, y2-y1) 
                
            except:
                self.hwnd=None
                print_exc()
                self.object.translation_ui.isbindedwindow=False
                self.object.translation_ui.refreshtooliconsignal.emit()
                pix = self.screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1) 
        else:
            pix = self.screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1) 
        return pix.toImage()
    def __init__(self,textgetmethod,object)  :
        self.screen = QApplication.primaryScreen()
        self.typename='ocr'
        self.savelastimg=None
        self.savelastrecimg=None
        self.savelasttext=None  
        self.object=object
        self.ending=False
        self.lastocrtime=0
        self.hwnd=None
        
        self.md5='0'
        self.sqlfname='./transkiroku/0_ocr.sqlite'
        self.sqlfname_all='./transkiroku/0_ocr.premt_synthesize.sqlite'
        self.jsonfname='./transkiroku/0_ocr.json'
        
        super(ocrtext,self ).__init__(textgetmethod) 
    def gettextthread(self ):
                 
            if self.object.rect is None:
                time.sleep(1)
                return None
            if self.object.rect[0][0]>self.object.rect[1][0] or self.object.rect[0][1]>self.object.rect[1][1]:
                time.sleep(1)
                return None
            time.sleep(0.1)
            #img=ImageGrab.grab((self.object.rect[0][0],self.object.rect[0][1],self.object.rect[1][0],self.object.rect[1][1]))
            #imgr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            imgr=self.imageCut(self.object.rect[0][0],self.object.rect[0][1],self.object.rect[1][0],self.object.rect[1][1])
            imgr.shape=imgr.height(),imgr.width(),imgr.depth()
            if globalconfig['mustocr'] and  time.time()-self.lastocrtime>globalconfig['mustocr_interval']:
                pass
            else:
                 
                
                if self.savelastimg is not None and  (imgr.shape==self.savelastimg.shape) : 
                    image_score = compareImage(imgr,self.savelastimg)
                else:
                    image_score=0
                self.savelastimg=imgr
                if image_score>0.95 : 
                    if self.savelastrecimg is not None and  (imgr.shape==self.savelastrecimg.shape   ) :

                        image_score2 = compareImage(imgr,self.savelastrecimg)
                    else:
                        image_score2=0
                    if image_score2>0.95:
                        return None
                    else: 
                        self.savelastrecimg=imgr
                else:
                    return  None 
            text=self.ocrtest(imgr) 
            if self.savelasttext is not None:
                sim=getEqualRate(self.savelasttext,text)
                #print('text',sim)
                if sim>0.9: 
                    return  None
            self.lastocrtime=time.time()
            self.savelasttext=text
            
            return (text)
            
    def runonce(self): 
        if self.object.rect is None:
            return
        if self.object.rect[0][0]>self.object.rect[1][0] or self.object.rect[0][1]>self.object.rect[1][1]:
            return  
        img=self.imageCut(self.object.rect[0][0],self.object.rect[0][1],self.object.rect[1][0],self.object.rect[1][1])
        
        

        text=self.ocrtest(img)
        self.textgetmethod(text,False)
    def ocrtest(self,img):
        use=None
        for k in globalconfig['ocr']:
            if globalconfig['ocr'][k]['use']==True:
                use=k
                break
        if use is None:
            return ''
        img.save('./capture/tmp.jpg')
        try:
            if use=='local':
                win32pipe.WaitNamedPipe("\\\\.\\Pipe\\ocrwaitsignal",win32con.NMPWAIT_WAIT_FOREVER)
                hPipe = win32file.CreateFile( "\\\\.\\Pipe\\ocrwaitsignal", win32con.GENERIC_READ | win32con.GENERIC_WRITE, 0,
                        None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None);
                #win32file.WriteFile(hPipe,'haha'.encode('utf8'))
                return (win32file.ReadFile(hPipe, 65535, None)[1].decode('utf8')).replace('\n','')
            else:
            
                ocr=importlib.import_module('otherocr.'+use).ocr 
                return ocr('./capture/tmp.jpg')
        except:
            print_exc()
            return ''