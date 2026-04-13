import streamlit as st
from rag import Ragservice
import config_data as config
st.title("智能机器")

st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"输入问题"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = Ragservice()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    a = []
    with st.spinner("loading..."):

        res = st.session_state["rag"].chain.stream({"input":prompt},config.session_config)
        st.chat_message("assistant").write(res)
        for chuank in res:
            a.append(chuank)

        st.session_state["message"].append({"role": "assistant", "content": "".join(a)})