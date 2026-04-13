from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="查询天气")
def tian()->str:
    return "明天是晴天"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[tian],
    system_prompt="你是一个温柔可爱,没有废话的美女助理"
)

res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"明天天气怎么样"}
        ]
    }
)

# print(res['messages'][-1].content)
for i in res['messages']:
    print(type(i).__name__,i.content)