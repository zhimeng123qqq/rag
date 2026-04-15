
import streamlit as st
import config_data as config
from agent import Reactagent

st.title("智能机器")

st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"输入问题"}]

if "agent" not in st.session_state:
    st.session_state["agent"] = Reactagent()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    a = []
    with st.spinner("loading..."):

        res = st.session_state["agent"].execute_stream(prompt)
        def gg(kk,aa):
            for k in kk:
                aa.append(k)
                yield k
        st.chat_message("assistant").write_stream(gg(res,a))


        st.session_state["message"].append({"role": "assistant", "content": "a[-1]"})

