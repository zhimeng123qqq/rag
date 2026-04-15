# -*- coding: utf-8 -*-
"""
将文件传入数据库
使用md5检测的好处不管文件多大（1KB 还是 10GB），MD5 永远是 32 位字符串
对比两个文件是否一样，不用逐字节对比，直接比 MD5 就行
速度极快、占用空间极小
"""

import os
from datetime import datetime

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as ca
import hashlib

def check_md5(md5_str):
    #
    if not os.path.exists(ca.md5_path): #
        open(ca.md5_path, 'w',encoding="utf-8").close() #创建空文件
        return False  #False 表示不存在

    else:
        for i in open(ca.md5_path,'r',encoding="utf-8").readlines():
            line = i.strip()
            if line == md5_str:
                return True
        return False

def save_md5(md5_str):
    with open(ca.md5_path,'a',encoding="utf-8") as f:
        f.write(md5_str+"\n")

def get_str_md5(string):
    byts_q =string.encode(encoding="utf-8") #还原字符串为2进制
    md5_obj = hashlib.md5()
    md5_obj.update(byts_q)
    kk = md5_obj.hexdigest()
    return kk

class KnowledgeBaseServres():
    def __init__(self):

        os.makedirs(ca.persist_directory,exist_ok=True)  #文件存在则跳过，否则创建

        self.chroma = Chroma(
            collection_name=ca.collection_name,
            embedding_function= DashScopeEmbeddings(model = ca.embedding_model_name),
            persist_directory=ca.persist_directory,    #chroma存储路经
        )

        self.spliter =RecursiveCharacterTextSplitter(
            chunk_size=ca.chunk_size,        #分割后的文本段长度
            chunk_overlap=ca.chunk_overlap,  #连续文本段的重叠字符数
            separators=ca.separators,        #段落划分的符号
            length_function=len,   #长度统计依据
        )     #文本分割器

    def upload_by_str(self,string,filename):

        md5_str=get_str_md5(string)
        if check_md5(md5_str):
            return "已经在库中"

        if len(string) > ca.max_len:
            new_list_str = self.spliter.split_text(string)
        else:
            new_list_str = [string]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小曹"
        }

        self.chroma.add_texts(
            new_list_str,
            metadatas=[metadata for _ in new_list_str],
        )   #存入向量库

        save_md5(md5_str)

        return "内容正在存入向量库中"






