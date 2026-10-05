---
name: autogen-agents
description: Use when autoGen multi-agent conversations — AssistantAgent, UserProxyAgent,
  group chat, code execution. Use when working with autogen agents.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- agents
- ai-agent
- autogen
- infrastructure
- memory
- self-improvement
version: 1.0.0
category: core
---


## Overview

AutoGen is a framework for building multi-agent conversation systems. Agents chat with each other to solve tasks, with built-in code execution, tool use, and human-in-the-loop patterns.

## Capabilities

- Create conversational agents with specific roles
- Enable code execution in sandboxed environments
- Build group chats with multiple agents
- Integrate function calling and tool use
- Support human-in-the-loop via UserProxyAgent
- Use nested conversations for complex workflows

## When to Use
**Trigger phrases:**
- "autogen agents"
- "AutoGen multi-agent conversations — AssistantAgent, UserProxyAgent, group chat, "


- Building conversational AI systems with multiple perspectives
- Needing agents that write and execute code
- Wanting human oversight in agent conversations
- Building research, coding, or analysis teams

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Basic Two-Agent Chat

```python
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

assistant = AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant.",
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # AUTO, ALWAYS, or NEVER
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": True},
)

user_proxy.initiate_chat(assistant, message="Write a Python script to analyze sales data.")
```

### Group Chat

```python
from autogen import GroupChat, GroupChatManager

coder = AssistantAgent(
    name="Coder",
    system_message="You write Python code. Always include complete, runnable code.",
    llm_config={"config_list": config_list},
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="You review code for bugs, security issues, and improvements.",
    llm_config={"config_list": config_list},
)

planner = AssistantAgent(
    name="Planner",
    system_message="You plan the approach and break tasks into steps.",
    llm_config={"config_list": config_list},
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "output"},
)

group_chat = GroupChat(
    agents=[user_proxy, planner, coder, reviewer],
    messages=[],
    max_round=20,
    speaker_selection_method="auto",  # or "round_robin", "random"
)

manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list})

user_proxy.initiate_chat(manager, message="Build a REST API for task management.")
```

### Function Calling

```python
from autogen import register_function

def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72°F, Sunny"

register_function(
    get_weather,
    caller=assistant,
    executor=user_proxy,
    name="get_weather",
    description="Get current weather for a city",
)
```

### Nested Conversations

```python
def writing_callback(recipient, messages, sender, config):
    """Check if writing meets criteria."""
    last_message = messages[-1]
    if "APPROVED" in last_message["content"]:
        return True, last_message["content"]
    return False, "Please revise and include APPROVED when done."

nested_assistant = AssistantAgent(
    name="nested_writer",
    llm_config={"config_list": config_list},
)

nested_assistant.register_nested_conversation(
    trigger=planner,
    recipient=nested_assistant,
    message="Write the technical documentation.",
    summary_method="last_msg",
    max_turns=5,
)
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `human_input_mode="NEVER"` | Fully autonomous execution |
| `human_input_mode="ALWAYS"` | Human approves every message |
| `human_input_mode="TERMINATE"` | Human only on completion |
| `code_execution_config` | Enable code writing + execution |
| `speaker_selection_method="auto"` | LLM picks next speaker |
| `register_function` | Add tool use to agents |
| Nested conversations | Subtask delegation |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Infinite loop | Agents keep responding | Set `max_consecutive_auto_reply` |
| Code execution failure | Syntax error or missing package | Check `work_dir` logs |
| Token limit | Long conversation | Reduce `max_round` or use summary |
| Group chat deadlock | No valid next speaker | Use `speaker_selection_method="round_robin"` |

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |