#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :frontend_streamlit.py
# @Time :2024/8/20 23:30
# @Author :张文军
# frontend_streamlit.py (前端 Streamlit 应用)
# 这个文件将使用 Streamlit 来创建一个用户界面，并通过 WebSocket 与后端进行实时通信。
import asyncio
import websockets
import streamlit as st
import json
import uuid

# Streamlit 应用的基本配置
st.title('WebSocket 聊天室')

# WebSocket 连接
ws_uri = "ws://localhost:8080"

# 默认的配置
default_llm_config = {
    "cache_seed": None,
    "model": "qwen-plus",
    "api_key": "sk-de6c4ff0d5d94975ac1f0f9961776ed5",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "temperature": 0.0,  # 更改为浮点数
    "max_tokens": 1024,
}

# 侧边栏配置
st.sidebar.header("LLM 配置")
cache_seed = st.sidebar.text_input("Cache Seed", value=default_llm_config["cache_seed"])
model = st.sidebar.text_input("Model Name", value=default_llm_config["model"])
api_key = st.sidebar.text_input("API Key", value=default_llm_config["api_key"])
base_url = st.sidebar.text_input("Base URL", value=default_llm_config["base_url"])
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,
                                value=float(default_llm_config["temperature"]), step=0.1)  # 使用float转换
max_tokens = st.sidebar.slider("Max Tokens", min_value=10, max_value=4096, value=default_llm_config["max_tokens"])

# 构建配置
custom_llm_config = {
    "cache_seed": cache_seed or default_llm_config["cache_seed"],
    "model": model or default_llm_config["model"],
    "api_key": api_key or default_llm_config["api_key"],
    "base_url": base_url or default_llm_config["base_url"],
    "temperature": temperature,
    "max_tokens": max_tokens,
}

# 构建完整的配置列表
config_list = [custom_llm_config]


async def send_message(message):
    global connection_active
    connection_active = True

    # 建立 WebSocket 连接
    websocket = await websockets.connect(ws_uri)
    try:
        # 发送消息
        await websocket.send(json.dumps({"content": message, "config_list": config_list}))

        # 接收并显示消息
        async for response in websocket:
            if not connection_active:
                break
            response_data = json.loads(response)

            # 添加用户和机器人的消息到聊天记录
            st.session_state.chat_records.append(('User', message))
            st.session_state.chat_records.append(('Bot', response_data['content']))

            # 更新聊天记录容器
            update_chat_records()

    except websockets.exceptions.ConnectionClosedOK:
        pass
    finally:
        if websocket and not websocket.closed:
            await websocket.close()
            connection_active = False


# 创建一个容器用于展示聊天记录和输入框
with st.container() as chat_container:
    # 创建一个容器用于存放聊天记录
    chat_records_container = st.empty()

    # 使用 Streamlit 的 state 来存储聊天记录
    if 'chat_records' not in st.session_state:
        st.session_state.chat_records = []

    # 创建一个唯一的 session ID 如果还没有的话
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # 获取唯一 key
    unique_key = st.session_state.session_id

    # 用户输入
    user_message = st.text_input("Enter your message:", key=f"input_{unique_key}")

    # 处理用户提交的消息
    if st.button('Send', key=f"send_{unique_key}"):
        if user_message:
            # 发送消息
            asyncio.run(send_message(user_message))

            # 清空输入框
            user_message = ""  # 将变量设为空，以便下次运行时输入框为空


def update_chat_records():
    chat_records_container.empty()
    for speaker, message in st.session_state.chat_records:
        chat_records_container.markdown(f"{speaker}: {message}")

    # 使用 JavaScript 滚动到底部
    st.write(
        '<script>setTimeout(function(){ document.querySelector(".main").scrollTo(0, document.querySelector(".main").scrollHeight); }, 500);</script>',
        unsafe_allow_html=True)


# 更新聊天记录容器
update_chat_records()
