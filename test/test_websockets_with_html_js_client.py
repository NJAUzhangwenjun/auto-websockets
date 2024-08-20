#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :test_websockets_with_html_js_client.py
# @Time :2024/8/20 23:03
# @Author :张文军
# 使用 HTML/JS 客户端测试 Websockets 服务器

# @Description :Websockets: 使用Websockets进行流式输入和输出
import asyncio
from datetime import datetime
from tempfile import TemporaryDirectory

from websockets.sync.client import connect as ws_connect
import uvicorn
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


def on_connect(iostream: IOWebsockets) -> None:
    """
    定义on_connect函数
        on_connect函数是利用websockets的应用程序的关键部分，它充当一个事件处理程序，每当建立新的客户端连接时就会调用。该函数旨在初始化任何必要的设置、通信协议或特定于新连接的数据交换过程。本质上，它为随后的交互会话奠定了基础，配置了服务器和客户端之间的通信方式，并在建立连接后采取了哪些初始操作。现在，让我们深入了解如何定义这个函数，特别是在使用AutoGen框架与websockets的上下文中。
        当客户端连接到websocket服务器时，服务器会自动初始化一个新的IOWebsockets类的实例。这个实例对于管理服务器和客户端之间的数据流至关重要。on_connect函数利用这个实例来设置通信协议、定义交互规则和

    示例中的on_connect函数的解释：
        接收初始消息：在建立连接后立即从客户端接收初始消息。这一步对于理解客户端的请求或启动对话流程至关重要。
        实例化ConversableAgent：使用特定的系统消息和LLM配置创建ConversableAgent的实例。如果你需要多个代理，请确保它们的llm_config不相同，因为向其中一个代理添加函数也会尝试将其添加到另一个代理中。
        实例化UserProxyAgent：类似地，创建UserProxyAgent实例，定义其终止条件、人工输入模式和其他相关参数。不需要定义llm_config，因为UserProxyAgent不使用LLM。
        定义特定于Agent的函数：如果你的对话代理需要特定的函数，可以在这一步定义。例如，定义一个获取城市天气预报的函数。
        启动对话：使用初始消息启动对话，将用户代理和对话代理传入。
    :param iostream:
    :return:
    """

    print(f" - on_connect(): 已连接到使用IOWebsockets的客户端 {iostream}", flush=True)

    print(" - on_connect(): 从客户端接收消息。", flush=True)

    # 1. 接收初始消息
    initial_msg = iostream.input()

    # 2. 实例化ConversableAgent
    agent = autogen.ConversableAgent(
        name="chatbot",
        system_message="完成分配给你的任务并在完成任务后回复TERMINATE。如果被问到天气，请使用工具'weather_forecast(city)'获取城市的天气预报。",
        llm_config=llm_config,
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
    user_proxy.initiate_chat(  # noqa: F704
        agent,
        message=initial_msg,
    )


"""
使用 HTML/JS 客户端测试 Websockets 服务器:

面提供的代码片段是一个示例，展示了如何使用 Python 内置的 http.server 模块创建一个交互式的测试环境，用于测试 on_connect 函数的功能。这个设置允许实时的交互。 在Web浏览器中实现交互，使开发人员能够以更用户友好和实用的方式测试websocket功能。以下是该代码的操作方式和潜在应用的详细说明：
 - 提供一个简单的HTML页面：代码首先定义了一个包含发送消息表单和显示传入消息的列表的HTML页面。使用JavaScript处理表单提交和websocket通信。
 - HTML文件的临时目录：创建一个临时目录来存储HTML文件。这种方法确保测试环境干净且隔离，最大程度地减少与现有文件或配置的冲突。
 - 自定义HTTP请求处理程序：定义了SimpleHTTPRequestHandler的自定义子类来提供HTML文件。该处理程序重写了do_GET方法，将根路径(/)重定向到chat.html页面，确保访问服务器根URL的访问者立即看到聊天界面。
 - 启动Websocket服务器：同时，在不同的端口上使用IOWebsockets.run_server_in_thread方法启动一个websocket服务器，以先前定义的on_connect函数作为新连接的回调。
 - HTML界面的HTTP服务器：实例化一个HTTP服务器来提供HTML聊天界面，使用户能够通过Web浏览器与websocket服务器进行交互。
 - 这个设置展示了将websocket与简单的HTTP服务器集成以创建动态和交互式Web应用程序的实际应用。通过使用Python的标准库模块，它演示了开发实时应用程序（如聊天系统、实时通知或交互式仪表板）的低门槛入门方法。
 - 从这个代码示例中可以得出的关键点是，Python的内置库可以轻松利用来原型设计和测试复杂的Web功能。对于希望构建真实世界应用程序的开发人员来说，这种方法提供了一种简单的方法来验证和完善websocket通信逻辑，然后再将其集成到更大的框架或系统中。这个测试设置的简单性和易用性使它成为开发各种交互式Web应用程序的绝佳起点。
:return:
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler  # noqa: E402
from tempfile import TemporaryDirectory
from pathlib import Path

PORT = 8000

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>自动生成的 WebSocket 测试</title>
    </head>
    <body>
        <h1>WebSocket 聊天室</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>发送</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8080/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

with TemporaryDirectory() as temp_dir:
    # 创建一个简单的 HTTP 网页
    path = Path(temp_dir) / "chat.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


    # 自定义HTTP请求处理程序：定义了SimpleHTTPRequestHandler的自定义子类来提供HTML文件。该处理程序重写了do_GET方法，将根路径(/)重定向到chat.html页面，确保访问服务器根URL的访问者立即看到聊天界面
    class MyRequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=temp_dir, **kwargs)

        def do_GET(self):
            if self.path == "/":
                self.path = "/chat.html"
            return SimpleHTTPRequestHandler.do_GET(self)


    handler = MyRequestHandler

    # 启动Websocket服务器：同时，在不同的端口上使用IOWebsockets.run_server_in_thread方法启动一个websocket服务器，以先前定义的on_connect函数作为新连接的回调。
    with IOWebsockets.run_server_in_thread(on_connect=on_connect, port=8080) as uri:
        print(f"WebSocket 服务器已启动，地址为 {uri}。", flush=True)
        # HTML界面的HTTP服务器：实例化一个HTTP服务器来提供HTML聊天界面，使用户能够通过Web浏览器与websocket服务器进行交互
        with HTTPServer(("", PORT), handler) as httpd:
            print("HTTP 服务器已启动，地址为 http://localhost:" + str(PORT))
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(" - HTTP 服务器已停止。", flush=True)
