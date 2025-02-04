from utils.config import globalconfig,static_data
import requests
from urllib.parse import quote
import re
from utils.utils import getproxy
from traceback import print_exc
class youdao:
    @property
    def srclang(self):
        
        try:
            l=static_data["language_list_translator_inner"][globalconfig['srclang3']]
            return l
             
        except:
            return ''
    def search(self,word):
        text=requests.get(f'https://dict.youdao.com/result?word={quote(word)}&lang={self.srclang}', proxies= getproxy()).text
        
        fnd=re.findall('<div class="head-content"(.*?)>([\\s\\S]*?)</span>(.*?)</div>',text)
        save=[] 
        try:
            asave=[]
            for ares  in fnd[0]:
                
                res=re.findall('>(.*?)<',ares+'<')
                for _ in res: 
                    for __ in _:
                        if __ !='':

                            asave.append(__)
            save.append(''.join(asave))
        except:
            print_exc()
         
        fnd=re.findall('<div class="each-sense"(.*?)>([\\s\\S]*?)</div></div></div>',text)
         
        try:
            for _,ares in fnd:
                asave=[]
                res=re.findall('>(.*?)<',ares+'<')
                for __ in res:
                    
                    if __ !='':

                        asave.append(__)
                save.append('<br>'.join(asave))
        except:
            print_exc()

        fnd=re.findall('<li class="word-exp"(.*?)>([\\s\\S]*?)</span></li>',text)
        try:
            for _,ares in fnd:
                asave=[]
                res=re.findall('>(.*?)<',ares+'<')
                for __ in res:
                    
                    if __ !='':

                        asave.append(__)
                 
                save.append('<br>'.join(asave))
        except:
            print_exc()
        return '<br><br>'.join(save)