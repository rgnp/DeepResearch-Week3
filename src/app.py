import streamlit as st
from agent import get_agent
from langchain_community.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="DeepResearch Agent", layout="wide")

st.title("🕵️‍♂️ DeepResearch: 全网深度研报 Agent")
st.caption("Week 3: Powered by DeepSeek & Tavily | Built with LangChain")

# 初始化消息历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "我是你的专属研究员。告诉我你想调研什么？（例如：'分析一下 2024 年 AI 手机的市场趋势'）"}
    ]

# 显示历史消息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 处理用户输入
if prompt := st.chat_input():
    # 1. 显示用户问题
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. AI 开始干活
    with st.chat_message("assistant"):
        # 🔥 关键组件：StreamlitCallbackHandler
        # 它会自动把 Agent 的 "思考过程" (调用搜索、读取结果) 渲染成漂亮的折叠框
        st_callback = StreamlitCallbackHandler(st.container())

        # 获取 Agent
        agent_executor = get_agent()

        # 执行！
        response = agent_executor.invoke(
            {"input": prompt},
            {"callbacks": [st_callback]} # 把回调传进去
        )

        # 显示最终结果
        st.write(response["output"])

        # 记入历史
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})