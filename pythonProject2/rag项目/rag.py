# -*- coding: utf-8 -*-
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, messages_from_dict, message_to_dict
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough, RunnableLambda
import config_data as config
from vector_stores import VectorStoreService
from langchain_core.prompts import  MessagesPlaceholder
import os
import json
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from knowledeg_base import KnowledgeBaseServres

# --------------------- 固定对话历史路径 ---------------------
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path =os.path.join(self.storage_path,f"{session_id}.json")
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    @property
    def messages(self) ->list[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                json_data=json.load(f)
                return messages_from_dict(json_data)

        except FileNotFoundError:
            return []

    def add_messages(self,messages):
        all_messages = list(self.messages)
        all_messages.extend(messages)
        new_messages=[message_to_dict(message) for message in all_messages]
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f,ensure_ascii=False) #把 Python 的列表 / 字典 转成json直接写入文件

    def clear(self) ->None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False)

def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")

# --------------------- RAG 服务（完全干净版） ---------------------
class Ragservice():
    def __init__(self):
        self.vec = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name),
        )
        self.prompt_t = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个温柔的美女助理，以参考资料为主，并根据历史消息回答问题，不知道就说不知道。参考资料：{context}"),
                ("system","历史消息如下"),
                MessagesPlaceholder(variable_name="history"),
                ("user", "{input}"),
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):

        retriever = self.vec.get_retriever()

        # 文档格式化函数
        def format_document(docs: list[Document]):
            if not docs:
                return "未找到相关资料"
            format_str=""
            for doc in docs:
                format_str += f"文档片段:{doc.page_content}\n 文档元数据:{doc.metadata}\n\n"
            return format_str

        def list_str(value):
            return value["input"]

        def history_str(value):
            new_value = {}
            new_value["history"] = value["input"]["history"]
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            return new_value
        base_chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(list_str) | retriever | format_document
            }
              | RunnableLambda(history_str)| self.prompt_t  |  self.chat_model |  StrOutputParser()
        )

        up_chain = RunnableWithMessageHistory(
            base_chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return up_chain

# --------------------- 测试运行 ---------------------
if __name__ == '__main__':
    service = Ragservice()
    session_config = {
        "configurable": {"session_id": "user_002"}
    }
    service = Ragservice()
    print("向量库当前文档总数：", service.vec.store_chroma._collection.count())

    res =Ragservice().chain.invoke({"input":"创建了文件，却没有找到文件怎么办"},session_config)
    print("最终回答：", res)

