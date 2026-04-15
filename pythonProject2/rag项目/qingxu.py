from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

import config_data as config


def qingxu_p(quar):
    if isinstance(quar, dict):
        user_input = quar.get("input", "")
        if isinstance(user_input, dict):
            user_input = user_input.get("input", str(user_input))
        elif user_input is None:
            user_input = str(quar)
    else:
        user_input = str(quar)
    prompt = ChatPromptTemplate.from_messages(
        [
        ("system", """
你是情绪识别器，只按规则返回单个英文单词，不许加任何多余文字、解释、标点。

规则：
- 开心、高兴、快乐、愉悦、兴奋、好笑 → 返回 funning
- 生气、愤怒、暴躁、不爽 → 返回 angry
- 无法判断、中性 → 返回 neutral
分析下面用户的情绪
"""),("user",user_input)
    ]
    )
    return prompt

def mood(query):
    if query=="funning":
        return "回答用户的方式加上开心的特点，例如输出：嘻嘻等开心修饰词的字样"
    if query=="neutral":
        return ""
    if query=="angry":
        return "回答用户的方式加上气愤的特点，例如输出：我真的生气了等开心修饰词的字样，用户辱骂时也会反击用户，如：用户说你算什么东西，则会回答：你又算什么东西，sb"


chat_model = ChatTongyi(model=config.chat_model_name)

# 创建情绪分析链 - 返回情绪词
def get_mood_style(mood_word):
    pass


qingxu_chain = (
    qingxu_p
    | chat_model
    | StrOutputParser()
    |RunnableLambda(mood)
  # 将情绪词转换为风格指导
)