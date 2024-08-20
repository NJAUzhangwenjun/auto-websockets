#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :backend_ws.py
# @Time :2024/8/20 23:29
# @Author :张文军
# backend_ws.py (后端 WebSocket 服务)
# 这个文件将负责处理 WebSocket 连接，并调用 on_connect 函数

import asyncio
import websockets
from datetime import datetime
import json
import autogen
from autogen.io.websockets import IOWebsockets

# LLM配置
llm_config = {
    "config_list": [
        {
            "cache_seed": None,
            "model": "qwen-plus",
            "api_key": "sk-de6c4ff0d5d94975ac1f0f9961776ed5",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "temperature": 0,
            "max_tokens": 1024,
        }
    ],
}


async def on_connect(iostream: IOWebsockets) -> None:
    """
    定义on_connect函数
    ...
    :param iostream:
    :return:
    """
    print(f" - on_connect(): 已连接到使用IOWebsockets的客户端 {iostream}", flush=True)

    print(" - on_connect(): 从客户端接收消息。", flush=True)

    # 1. 接收初始消息
    try:
        initial_msg = await iostream.input()  # 使用 await 等待输入完成
        initial_msg = json.loads(initial_msg)
        print(f" - on_connect(): 收到初始消息: {initial_msg}", flush=True)
        config_list = initial_msg.get("config_list", llm_config["config_list"])
    except Exception as e:
        print(f" - on_connect(): 处理初始消息时发生错误: {e}", flush=True)
        return

    # 2. 实例化ConversableAgent
    agent = autogen.ConversableAgent(
        name="chatbot",
        system_message="完成分配给你的任务并在完成任务后回复TERMINATE。如果被问到天气，请使用工具'weather_forecast(city)'获取城市的天气预报。",
        llm_config=config_list[0],  # 使用从客户端接收到的配置列表的第一个配置
    )

    # 3. 定义UserProxyAgent
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        system_message="用户的代理。",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config=False,
    )

    # 4. 定义特定于Agent的函数
    def weather_forecast(city: str) -> str:
        return f"{datetime.now()}时{city}的天气预报是晴朗。"

    autogen.register_function(
        weather_forecast, caller=agent, executor=user_proxy, description="城市的天气预报"
    )

    # 5. 启动对话
    print(
        f" - on_connect(): 使用消息'{initial_msg}'与代理{agent}启动对话",
        flush=True,
    )
    user_proxy.initiate_chat(
        agent,
        message=initial_msg["content"],
    )


async def handle_connection(websocket, path):
    # 当客户端连接时调用此函数
    try:
        await on_connect(IOWebsockets(websocket))  # 使用 await 调用 on_connect
    except Exception as e:
        print(f" - handle_connection(): 处理连接时发生错误: {e}", flush=True)


start_server = websockets.serve(handle_connection, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
