#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :simple_chat.py.py
# @Time :2024/8/21 00:54
# @Author :张文军
# 设置数据集路径
from autogen import ConversableAgent, UserProxyAgent, config_list_from_json, AssistantAgent
from config_llm import llm_config
from autogen.coding import LocalCommandLineCodeExecutor


def main():
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample.
    # For example, if you have created a OAI_CONFIG_LIST file in the current working directory, that file will be used.

    # Create the agent that uses the LLM.
    assistant = AssistantAgent(
        "agent",
        llm_config=llm_config,
        code_execution_config={"executor": LocalCommandLineCodeExecutor()},
        max_consecutive_auto_reply=3,
        human_input_mode="TERMINATE"
    )

    # Create the agent that represents the user in the conversation.
    user_proxy = UserProxyAgent("user", code_execution_config=False)
    user_proxy.register_reply(

    )

    # Let the assistant start the conversation.  It will end when the user types exit.
    user_proxy.initiate_chat(assistant, message="今天是多少号?")


if __name__ == "__main__":
    main()
