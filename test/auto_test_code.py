import unittest

import os

import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, Cache

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


class MyTestCase(unittest.TestCase):

    # 测试LLM
    def test_llm(self):
        assistant = AssistantAgent("assistant", llm_config=llm_config)
        user_proxy = UserProxyAgent(
            "user_proxy",
            code_execution_config={"executor": LocalCommandLineCodeExecutor()}
        )

        def print_messages(recipient, messages, sender, config):
            if "callback" in config and config["callback"] is not None:
                callback = config["callback"]
                callback(sender, recipient, messages[-1])
            print(f"Messages sent to: {recipient.name} | num messages: {len(messages)}")
            return False, None  # required to ensure the agent communication flow continues

        user_proxy.register_reply(
            [autogen.Agent, None],
            reply_func=print_messages,
            config={"callback": None},
        )

        # 开始对话
        with Cache.disk(
                cache_path_root="/Users/zhangwenjun/Documents/javaFiles/agents/pythonProject/autogen_cache") as cache:
            user_proxy.initiate_chat(assistant, message="今天是周几?", cache=cache)

    """
    代码生成、执行和调试的任务解决
    """

    def test_code(self):
        AssistantAgent.DEFAULT_SYSTEM_MESSAGE = AssistantAgent.DEFAULT_SYSTEM_MESSAGE + "\n Note: You must always respond in Chinese."
        # 创建一个名为“assistant”的AssistantAgent实例
        assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config=llm_config
        )

        # 创建一个名为“user_proxy”的UserProxyAgent实例
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            # 检查消息内容是否以"TERMINATE"结尾,以确定是否终止对话
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "executor": LocalCommandLineCodeExecutor(work_dir="../coding"),  # 用于运行生成的代码的执行器,并指定工作目录
            },
        )
        # assistant接收来自user_proxy的消息，其中包含任务描述
        chat_res = user_proxy.initiate_chat(
            assistant,
            clear_history=False,
            message="""今天是几号？比较META和TESLA的年初至今收益。""",
            summary_method="reflection_with_llm",  ## 使用LLM进行总结
        )
        # 打印结果
        print(f'summary={chat_res.summary}')

        #



if __name__ == '__main__':
    unittest.main()
