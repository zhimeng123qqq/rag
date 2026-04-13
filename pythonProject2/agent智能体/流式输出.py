from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="查询天气")
def tian()->str:
    return "明天是雨天"

@tool(description="查询温度")
def wen()->str:
    return "明天是30°"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[tian,wen],
    system_prompt="你是一个温柔可爱,没有废话的美女助理，并会说明调用了哪些工具"
)

res =agent.stream(
    {"messages":[{"role":"user","content":"明天会下雨吗，适合穿毛衣吗"}]},
    stream_mode="values"
)

for chunk in res:
    messages = chunk.get("messages", [])
    if not messages:
        continue

    last_msg = messages[-1]

    # 1. 输出 AI 回答内容
    if last_msg.content:
        print(f"回答：{last_msg.content}")

    # 2. 输出 工具调用信息（核心！）
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        for tool_call in last_msg.tool_calls:
            tool_name = tool_call["name"]
            print(f"✅ 调用工具：{tool_name}")



