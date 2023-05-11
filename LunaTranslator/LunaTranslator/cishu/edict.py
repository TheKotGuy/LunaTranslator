from utils.config import globalconfig
import sqlite3,os
import winsharedutils,re
from utils.utils import argsort
from traceback import print_exc
class edict():
    def __init__(self):
        self.sql=None
        try:
            path=(globalconfig['cishu']['edict']['path'] )
            if os.path.exists(path):
                self.sql=sqlite3.connect( path,check_same_thread=False)
        except:
            pass
    def end(self):
         self.sql.close()
    def search(self,word):
          
                x=self.sql.execute(f"select text, entry_id from surface where  text like '%{word}%'")
                exp=x.fetchall()
                dis=9999
                dis=[]
                for w,xx in exp: 
                    d=winsharedutils.distance(w,word)
                    dis.append(d)
                save=[]
                srt=argsort(dis)
                for ii in srt:
                    if exp[ii][1] not in save:
                        save.append(exp[ii][1])
                    if len(save)>=10:
                        break
                saveres=[]
                for _id in save:
                    x=self.sql.execute(f"select word, content from entry where  id ={_id}").fetchone()
                    saveres.append(x[0]+'<br>'+re.sub('/EntL.*/','', x[1][1:]))
                
                return '<hr>'.join(saveres)
            