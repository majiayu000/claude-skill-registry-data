---
name: autogen
description: Build conversational multi-agent systems with AutoGen (AG2) — define AssistantAgent and UserProxyAgent, set up GroupChat with GroupChatManager for round-robin or auto routing, enable code execution, and compose nested chats or sequential pipelines.
triggers:
  - "autogen"
  - "ag2"
  - "pyautogen"
  - "autogen agent"
  - "autogen groupchat"
  - "assistant agent user proxy"
  - "groupchatmanager"
  - "autogen code execution"
  - "autogen conversable agent"
  - "multi agent conversation autogen"
  - "autogen nested chat"
  - "autogen swarm"
do_not_use_for:
  - Role-playing agent crews — use crewai instead
  - State graph agents — use langgraph instead
  - Type-safe single agents — use pydantic-ai instead
see_also:
  - crewai
  - langgraph
  - smolagents
---

# AutoGen (AG2) — Conversational Multi-Agent Framework

**Source:** ag2ai/ag2 (Apache 2.0) — formerly microsoft/autogen; conversational agent orchestration

## Core Concepts

| Component | Description |
|-----------|-------------|
| `ConversableAgent` | Base class — can send/receive messages, use LLM, execute code |
| `AssistantAgent` | LLM-powered agent; generates replies using the model |
| `UserProxyAgent` | Proxy for human input; can auto-execute code |
| `GroupChat` | Manages conversation between multiple agents |
| `GroupChatManager` | Routes messages in a GroupChat (round-robin or auto) |

## Install

```bash
pip install ag2
# Optional: code execution support
pip install ag2[jupyter-executor]
```

## Two-Agent Conversation

```python
import autogen

config_list = [
    {
        "model": "claude-sonnet-4-5",
        "api_key": "your-anthropic-key",
        "api_type": "anthropic",
    }
]

llm_config = {"config_list": config_list, "cache_seed": 42}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant.",
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",   # NEVER | ALWAYS | TERMINATE
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,  # no code execution
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate Fibonacci numbers.",
)
```

## Code Execution Agent

```python
import autogen

llm_config = {"config_list": [{"model": "claude-sonnet-4-5", "api_key": "..."}]}

assistant = autogen.AssistantAgent(
    name="coder",
    llm_config=llm_config,
    system_message="Write Python code to solve tasks. Reply TERMINATE when done.",
)

user_proxy = autogen.UserProxyAgent(
    name="executor",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # True for Docker isolation (recommended)
    },
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

user_proxy.initiate_chat(
    assistant,
    message="Create and run a script that plots a sine wave using matplotlib.",
)
```

## GroupChat (Multiple Agents)

```python
import autogen

llm_config = {"config_list": [{"model": "claude-sonnet-4-5", "api_key": "..."}]}

planner = autogen.AssistantAgent(
    name="Planner",
    system_message="You break down tasks into steps and create a plan.",
    llm_config=llm_config,
)

coder = autogen.AssistantAgent(
    name="Coder",
    system_message="You implement the code based on the plan.",
    llm_config=llm_config,
)

reviewer = autogen.AssistantAgent(
    name="Reviewer",
    system_message="You review code for bugs and suggest improvements.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding", "use_docker": False},
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, coder, reviewer],
    messages=[],
    max_round=12,
    speaker_selection_method="auto",  # LLM selects next speaker
    # or: "round_robin" | custom function
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

user_proxy.initiate_chat(
    manager,
    message="Build a REST API endpoint for user authentication.",
)
```

## Custom Speaker Selection

```python
def custom_speaker_selection(last_speaker, groupchat):
    """Custom logic to select next speaker."""
    messages = groupchat.messages
    if last_speaker.name == "Planner":
        return groupchat.agent_by_name("Coder")
    elif last_speaker.name == "Coder":
        return groupchat.agent_by_name("Reviewer")
    else:
        return groupchat.agent_by_name("Planner")

groupchat = autogen.GroupChat(
    agents=[planner, coder, reviewer],
    messages=[],
    speaker_selection_method=custom_speaker_selection,
)
```

## Nested Chat (Subpipeline)

```python
import autogen

llm_config = {"config_list": [{"model": "claude-sonnet-4-5", "api_key": "..."}]}

# Inner pipeline: writer + reviewer
inner_writer = autogen.AssistantAgent("inner_writer", llm_config=llm_config)
inner_reviewer = autogen.AssistantAgent("inner_reviewer", llm_config=llm_config)
inner_proxy = autogen.UserProxyAgent("inner_proxy", human_input_mode="NEVER",
                                      max_consecutive_auto_reply=3)

# Outer agent triggers nested chat
outer_assistant = autogen.AssistantAgent("outer_assistant", llm_config=llm_config)
outer_proxy = autogen.UserProxyAgent(
    "outer_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

# Register nested chat — runs when outer_assistant replies to outer_proxy
outer_proxy.register_nested_chats(
    [{"sender": inner_proxy, "recipient": inner_writer, "max_turns": 3}],
    trigger=outer_assistant,
)

outer_proxy.initiate_chat(outer_assistant, message="Write and review a blog post on AI.")
```

## Swarm (Handoff Pattern)

```python
from autogen import SwarmAgent, initiate_swarm_chat, ON_CONDITION, AFTER_WORK, SwarmResult

def check_order(product: str, order_id: str) -> SwarmResult:
    """Check order status."""
    status = lookup_order(order_id)  # your implementation
    return SwarmResult(values=f"Order {order_id}: {status}", agent=billing_agent)

def process_refund(order_id: str, reason: str) -> str:
    """Process a refund request."""
    execute_refund(order_id)
    return "Refund processed successfully."

triage_agent = SwarmAgent(
    name="Triage",
    system_message="Determine if user needs order status or refund.",
    llm_config=llm_config,
    functions=[check_order],
)

billing_agent = SwarmAgent(
    name="Billing",
    system_message="Handle refunds and billing questions.",
    llm_config=llm_config,
    functions=[process_refund],
    after_work=AFTER_WORK.TERMINATE,
)

# Handoff: triage → billing based on function result
chat_result, context, last_agent = initiate_swarm_chat(
    initial_agent=triage_agent,
    agents=[triage_agent, billing_agent],
    messages="I want to return my order #12345",
    max_rounds=10,
)
```

## Structured Output

```python
from pydantic import BaseModel
import autogen

class CodeReview(BaseModel):
    has_bugs: bool
    severity: str
    suggestions: list[str]

llm_config = {
    "config_list": [{"model": "claude-sonnet-4-5", "api_key": "..."}],
    "response_format": CodeReview,  # enforces Pydantic schema
}

reviewer = autogen.AssistantAgent("reviewer", llm_config=llm_config)
```

## Anti-Fake-Pass Checks

- [ ] `human_input_mode="NEVER"` needed for fully automated runs — default is "ALWAYS"
- [ ] `is_termination_msg` must be set or conversation runs until `max_consecutive_auto_reply`
- [ ] `code_execution_config` on `UserProxyAgent`, NOT on `AssistantAgent`
- [ ] `GroupChatManager` requires `llm_config` to select speakers with `"auto"` mode
- [ ] Nested chats trigger on reply FROM the specified `trigger` agent — not on any message
- [ ] `SwarmResult(agent=next_agent)` is how swarm handoffs are declared — return from function
- [ ] `speaker_selection_method="auto"` costs extra LLM calls per round to pick next speaker
