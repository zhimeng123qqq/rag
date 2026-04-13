# -*- coding: utf-8 -*-
""" web网页上传文件"""
#streamlit run D:/zhuomian/rag项目/pythonProject2/rag项目/app_file_upload.py

import os
import time

import streamlit as st
from PyPDF2 import PdfReader

from knowledeg_base import KnowledgeBaseServres

st.title("文件上传")

uplode_file=st.file_uploader(
    "上传文件",
    type=["txt","pdf"],
    accept_multiple_files=False,# 可接受1个文件上传
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseServres()

if uplode_file is not None:
    file_name = uplode_file.name
    file_type = uplode_file.type
    file_size = uplode_file.size / 1024  #KB

    st.subheader(f"文件名称: {file_name}")
    st.write(f"文件类型|大小: {file_type}|{file_size:.2f}KB")

    text = ""
    try:
        # 1. 如果是 TXT 文件
        if file_name.endswith(".txt"):
            text = uplode_file.getvalue().decode("utf-8")

        # 2. 如果是 PDF 文件（提取所有页面文字）
        elif file_name.endswith(".pdf"):
            pdf_reader = PdfReader(uplode_file)
            # 遍历所有页面提取文本
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # 显示提取的文本预览
        st.subheader("提取的文本内容预览")
        st.text_area("文本内容", text, height=300)

        # 存入向量库
        with st.spinner("正在提取文本并入库......"):
            time.sleep(1)
            res = st.session_state["service"].upload_by_str(text, file_name)
            st.success("处理完成！")
            st.write(res)

    except Exception as e:
        st.error(f"文件处理失败：{str(e)}")






