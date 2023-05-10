import os
from ctypes import  c_uint,pointer 
import winsharedutils
from utils.config import _TR 

from utils import somedef
from ocrengines.baseocrclass import baseocr  
class OCR(baseocr):
    def initocr(self):        
        num=c_uint()
        ret=winsharedutils.getlanguagelist(pointer(num))
        _allsupport=[]
        for i in range(num.value):
            _allsupport.append(ret[i])
        self.supportmap={}
        for lang in somedef.language_list_translator_inner+['zh-Hans','zh-Hant']:
            if lang=='zh' or lang=='cht':continue
            for s in _allsupport:
                if s.startswith(lang) or lang.startswith(s):
                    self.supportmap[lang]=s
                    break
        if 'zh-Hans' in self.supportmap:
            v=self.supportmap.pop('zh-Hans')
            self.supportmap['zh']=v
        if 'zh-Hant' in self.supportmap:
            v=self.supportmap.pop('zh-Hant')
            self.supportmap['cht']=v
    def ocr(self,imgfile):  
        if self.srclang not in self.supportmap: 
            idx=somedef.language_list_translator_inner.index(self.srclang)
            raise Exception(_TR('系统未安装')+_TR(somedef.language_list_translator[idx])+_TR('的OCR模型'))
        
        if self.srclang in ['zh','ja','cht']:
            space=''
        else:
            space=' '
        num=c_uint()
        ress={}
        ress2=[]  
        ret=winsharedutils.OCR_f(os.path.abspath(imgfile),self.supportmap[self.srclang],space,pointer(num))
        for i in range(num.value): 
        
            ress2.append( ret.lines[i])
            ress[ress2[-1]]=ret.ys[i]
        ress2.sort(key= lambda x:ress[x])

            
        xx=self.space.join(ress2) 
        return xx
        