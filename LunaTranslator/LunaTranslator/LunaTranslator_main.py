import sys
from PyQt5.QtCore import QCoreApplication ,Qt 
from PyQt5.QtWidgets import  QApplication
import os
import platform,os
def initpath(): 
    dirname=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dirname) 

    if os.path.exists('./userconfig')==False:
        os.mkdir('./userconfig')
    if os.path.exists('./userconfig/memory')==False:
        os.mkdir('./userconfig/memory')
    if os.path.exists('./translation_record')==False:
        os.mkdir('./translation_record') 
    if os.path.exists('./translation_record/cache')==False:
        os.mkdir('./translation_record/cache') 
    if os.path.exists('./cache')==False:
        os.mkdir('./cache')
    if os.path.exists('./cache/ocr')==False:
        os.mkdir('./cache/ocr')
    if os.path.exists('./cache/update')==False:
        os.mkdir('./cache/update')
    if os.path.exists('./cache/screenshot')==False:
        os.mkdir('./cache/screenshot')
    if os.path.exists('./cache/tts')==False:
        os.mkdir('./cache/tts')

    sys.path.append('./userconfig')
   

if __name__ == "__main__" :
    initpath()
    from utils.config import _TR,static_data
    from gui.usefulwidget import getQMessageBox
    from LunaTranslator import MAINUI
    from utils.hwnd import  getScreenRate  

    screenrate=getScreenRate()   
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) 

    js=static_data['checkintegrity']
    flist=js['shared']
    if platform.architecture()[0]=="64bit":
        flist+=js['64']
    else:
        flist+=js['32']
    collect=[] 
    for f in flist:
        if os.path.exists(f)==False:
            collect.append(f)
    if len(collect):
        getQMessageBox(None,_TR("错误"),_TR("找不到重要组件：")+"\n"+"\n".join(collect)+"\n"+_TR("请重新下载并关闭杀毒软件后重试"))
        os._exit(0) 
    
    
    
 
    main = MAINUI(app) 
    main.screen_scale_rate =screenrate
    main.checklang() 
    main.aa() 
    app.exit(app.exec_())
