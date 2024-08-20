#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :autogen_builder_test.py
# @Time :2024/8/21 01:47
# @Author :张文军
# 设置数据集路径
import autogen

config_file_or_env = '/Users/zhangwenjun/Documents/javaFiles/agents/pythonProject/config_list.json'  # 修改路径
default_llm_config = {
    "cache_seed": None,
    "model": "qwen-plus",
    "api_key": "sk-xxxx",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "temperature": 0,
    "max_tokens": 1024,
    "price": [0.004, 0.006]
}

from autogen.agentchat.contrib.agent_builder import AgentBuilder

builder = AgentBuilder(config_file_or_env=config_file_or_env, builder_model='qwen-plus', agent_model='qwen-plus')


#
# building_task = "今天上海的天气预报如何？"
#
# agent_list, agent_configs = builder.build(building_task, default_llm_config, coding=True)
#
# import autogen
#
#
def start_task(execution_task: str, agent_list: list, llm_config: dict):
    config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["qwen-plus"]})

    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}
    )
    agent_list[0].initiate_chat(manager, message=execution_task)


new_builder = AgentBuilder(config_file_or_env=config_file_or_env)
agent_list, agent_config = new_builder.load('/Users/zhangwenjun/Documents/javaFiles/agents/pythonProject/test/save_config_146a0be157b770c7d6e880a0e9c465d5.json')

start_task(
    execution_task="天津今天的天气如何?",
    agent_list=agent_list,
    llm_config=default_llm_config
)

builder.clear_all_agents(recycle_endpoint=True)

saved_path = builder.save()
