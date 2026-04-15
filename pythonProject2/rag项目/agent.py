from langchain.agents import create_agent
import config_data as ca
from agent_tools import vector_summarise
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents.middleware import ToolRetryMiddleware
class Reactagent():
    def __init__(self):
        self.agent = create_agent(
            model = ChatTongyi(model=ca.chat_model_name),
            system_prompt="""
                        你是一个智能助手，必须优先使用 vector_summarise 工具检索知识库回答用户问题。
                        不要编造答案，必须使用检索到的资料,如果不能检索到资料，可以适当发挥。""",
            tools=[vector_summarise],
            middleware=[ToolRetryMiddleware()]
        )

    def execute_stream(self,query):
        input_dict={
            "messages":[
                {"role":"user","content":query},
            ]
        }

        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False}):
            last_message = chunk["messages"][-1]
            if last_message.content:
                yield last_message.content.strip() + "\n"




if __name__ == '__main__':
    agent = Reactagent()
    for res in agent.execute_stream("我身高145，体重30kg，尺码推荐"):
        print(res,end="",flush=True)


