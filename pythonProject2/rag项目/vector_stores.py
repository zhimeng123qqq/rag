# -*- coding: utf-8 -*-
from langchain_classic.retrievers import EnsembleRetriever
import config_data as ca
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_community.embeddings import DashScopeEmbeddings
class VectorStoreService():
    def __init__(self):
        self.embedding = DashScopeEmbeddings(model=ca.embedding_model_name)

        self.store_chroma =Chroma(
            collection_name=ca.collection_name,
            embedding_function=self.embedding,
            persist_directory=ca.persist_directory,
        )

    def get_retriever(self):

        return self.store_chroma.as_retriever(search_kwargs={"k": ca.similarity})

    #实现检索优化


if __name__ == '__main__':
    a = VectorStoreService().get_retriever()
    res =a.invoke("我身高145，体重35GK，尺码推荐")
    print(res)
