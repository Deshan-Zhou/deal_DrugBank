from xml.sax.handler import ContentHandler
from xml.sax import parse
import pandas as pd
"""
简写：
dbid : DrugBank id
dbname : DrugBank name
chid : ChEMBL id
ptid : protein id
"""
class ExtractData(ContentHandler):

    def __init__(self):
        #各个简写的映射关系
        self.dbid_chid = {}
        self.dbid_dbname = {}
        self.dbid_dbid = {}
        self.dbid_ptid = {}
        #当前的药物id和遍历区域的限定
        self.curr_id = ""
        self.limit = 0

    #可以自动获取遍历到的元素里面的内容，如<ele>content.....</ele>
    def characters(self,content):
        if self.limit == 2:
            self.curr_id = content
            self.limit = 3

        elif self.limit == 4:
            self.dbid_dbname[self.curr_id] = content
            self.limit = 0

        elif self.limit == 6:
            self.dbid_dbid.setdefault(self.curr_id,set()).add(content)
            self.limit = 5

        elif self.limit == 8:
            if content == "ChEMBL":
                self.limit = 9

        elif self.limit == 10:
            self.dbid_chid[self.curr_id] = content
            self.limit = 0

    #遍历到标签开始时调用        
    def startElement(self,name,attrs):
        if name == "drug":
            self.limit = 1
            
        if self.limit == 1 and name == "drugbank-id" and attrs:
            if attrs["primary"] == "true":
                self.limit = 2

        elif self.limit == 3 and name=="name":
            self.limit = 4

        elif name == "drug-interactions":
            self.limit = 5
        
        elif self.limit == 5 and name == "drugbank-id":
            self.limit = 6

        elif name == "targets":
            self.limit = 7

        elif self.limit == 7 and name == "polypeptide":
            self.dbid_ptid.setdefault(self.curr_id,set()).add(attrs["id"])

        elif name == "resource" and self.limit!=7:
            self.limit= 8

        elif self.limit == 9 and name == "identifier":
            self.limit = 10
            
    #遍历到标签结束时调用  
    def endElement(self,name):
        if name == "drug-interactions":
            self.limit = 0
            
        elif name == "targets":
            self.limit = 0
    #遍历结束时调用
    def endDocument(self):
        #DrugBank id和ChEMBL id的映射
        list1_key=[]
        list1_val=[]
        list1_columns="ChEMBL_id",
        for key,val in self.dbid_chid.items():
            list1_key.append(key)
            list1_val.append(val)
        file1=pd.DataFrame(index=list1_key,columns=list1_columns,data=list1_val)
        file1.to_csv('dbid_chid.csv')

        #DrugBank id和drug name的映射
        list2_key=[]
        list2_val=[]
        list2_columns="Drug_name",
        for key,val in self.dbid_dbname.items():
            list2_key.append(key)
            list2_val.append(val)
        file2=pd.DataFrame(index=list2_key,columns=list2_columns,data=list2_val)
        file2.to_csv('dbid_dbname.csv')

#这个映射关系太多，后期再处理
#        for data in self.dbid_dbid.items():
#            print(3,data)

        #DrugBank id和target id的相互作用映射
        list4_key=[]
        list4_val=[]
        for key,val in self.dbid_ptid.items():
            list4_key.append(key)
            list4_val.append(list(val))
        file4=pd.DataFrame(index=list4_key,data=list4_val)
        file4.to_csv('dbid_ptid.csv')


parse('full database.xml',ExtractData())
