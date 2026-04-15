from langchain_core.tools import tool
from vector_stores import VectorStoreService


@tool(description="从向量库中检索参考资料")
def vector_summarise(query:str) ->str:
    vector = VectorStoreService()
    a = vector.get_retriever()
    res = a.invoke(query)
    return res

@tool(description="获取用户ID，以纯字符串返回")
def get_userID() ->str:
    pass


@tool(description="从外部系统中获取用户的使用记录，以纯字符串返回，没有找到返回空字符串")
def vector_dd() ->str:
    pass

