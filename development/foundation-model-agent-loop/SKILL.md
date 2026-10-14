---
name: foundation-model-agent-loop
description: "Canonical pattern for building an agentic tool-calling loop using a Databricks-hosted Foundation Model. Use when creating agent_loop.py or any backend that calls a Foundation Model with function-calling to orchestrate tools."
metadata:
  author: stayfinder-team
  version: "1.0"
compatibility: "Databricks Apps, Foundation Models with function-calling support"
---

# Foundation Model Agent Loop

A plain Python agentic loop that calls a Databricks-hosted Foundation Model
with tool definitions. The model decides which tools to call; your code
executes them and feeds results back until the model produces a final text
response.

**No LangGraph, no MLflow, no custom model deployment** — just HTTP calls.

## When to Use This Skill

Use this skill when:
- Building a backend agent that uses a Databricks Foundation Model (e.g.,
  `databricks-meta-llama-3-3-70b-instruct`) as the "brain"
- The agent needs to call tools (Genie, business logic, external APIs)
  based on user input
- You want the model to decide routing — no hand-written if/else classifiers

## Prerequisites

- A Databricks-hosted Foundation Model endpoint that supports function calling
- `databricks-sdk` and `requests` Python packages
- Valid Databricks authentication (`Config()` from the SDK)

## Architecture

```
User Message
    │
    ▼
┌─────────────────────────────────────┐
│  Build messages list:               │
│    [system_prompt, user_message]    │
│  + tool definitions (TOOL_SCHEMAS)  │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │  POST to Foundation  │◄──────────────────────┐
    │  Model endpoint      │                       │
    └──────────┬───────────┘                       │
               │                                   │
    ┌──────────▼───────────┐                       │
    │  Parse response:     │                       │
    │  choices[0].message  │                       │
    └──────────┬───────────┘                       │
               │                                   │
    ┌──────────▼───────────┐     ┌─────────────┐   │
    │  Has tool_calls?     │─YES─│ Execute each │   │
    │  finish_reason?      │     │ tool locally │   │
    └──────────┬───────────┘     └──────┬──────┘   │
               │ NO                     │          │
               │              Append tool results  │
    ┌──────────▼───────────┐  to messages list     │
    │  Return final text   │        │              │
    │  content to user     │        └──────────────┘
    └──────────────────────┘
```

## Canonical Implementation

### Step 1: Define tool schemas (OpenAI function-calling format)

```python
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "query_genie",
            "description": "Query the accommodation database using natural language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "A natural-language question about the data",
                    }
                },
                "required": ["question"],
            },
        },
    },
    # ... more tools
]
```

### Step 2: Create a dispatch map

```python
from myapp.tools.genie_tool import query_genie_fn
from myapp.tools.custom_tools import calculate_price_fn

TOOL_FUNCTIONS = {
    "query_genie": query_genie_fn,
    "calculate_price": calculate_price_fn,
}
```

### Step 3: Call the Foundation Model endpoint

```python
import requests
from databricks.sdk.core import Config

def _call_foundation_model(messages, tools=None):
    cfg = Config()
    headers = cfg.authenticate()
    headers["Content-Type"] = "application/json"

    host = str(cfg.host).rstrip("/")
    endpoint = os.getenv("LLM_ENDPOINT_NAME", "databricks-meta-llama-3-3-70b-instruct")
    url = f"{host}/serving-endpoints/{endpoint}/invocations"

    payload = {"messages": messages, "max_tokens": 1024}
    if tools:
        payload["tools"] = tools

    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    return resp.json()
```

### Step 4: Implement the agent loop

```python
import json

MAX_ITERATIONS = 10

def run_agent_loop(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(MAX_ITERATIONS):
        try:
            response = _call_foundation_model(messages, tools=TOOL_SCHEMAS)
        except Exception as exc:
            return f"Error connecting to AI service: {exc}"

        choices = response.get("choices", [])
        if not choices:
            return "Unexpected response from AI service."

        assistant_msg = choices[0].get("message", {})
        finish_reason = choices[0].get("finish_reason", "")

        # Always append the assistant message to maintain conversation history
        messages.append(assistant_msg)

        # Check: does the model want to call tools?
        tool_calls = assistant_msg.get("tool_calls")

        if not tool_calls or finish_reason == "stop":
            # No tool calls — return the final text response
            return assistant_msg.get("content", "No response generated.")

        # Execute each tool call
        for tc in tool_calls:
            tool_name = tc["function"]["name"]
            raw_args = tc["function"]["arguments"]

            # Parse arguments (model returns them as a JSON string)
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
            except json.JSONDecodeError:
                args = {}

            # Execute the tool
            fn = TOOL_FUNCTIONS.get(tool_name)
            if fn:
                try:
                    result = fn(**args)
                except Exception as exc:
                    result = json.dumps({"error": str(exc)})
            else:
                result = json.dumps({"error": f"Unknown tool: {tool_name}"})

            # Ensure result is a string
            if not isinstance(result, str):
                result = json.dumps(result, default=str)

            # Append tool result to conversation — MUST include tool_call_id
            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": result,
            })

        # Loop continues: model receives tool results and decides next action

    return "Too many steps. Please try a simpler query."
```

## Critical Details

### Response format from Foundation Model

The Foundation Model returns OpenAI-compatible responses:
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Here are apartments in Austin...",
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "query_genie",
              "arguments": "{\"question\": \"Find apartments in Austin under $200\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

Key fields:
- `choices[0].message.tool_calls` — present when the model wants to call tools
- `choices[0].message.content` — present when the model has a final text response
- `choices[0].finish_reason` — `"stop"` for final response, `"tool_calls"` for tool requests
- `tool_calls[].id` — must be passed back as `tool_call_id` in the tool result message
- `tool_calls[].function.arguments` — a **JSON string** (not a dict), must be parsed

### Tool result message format

When returning tool results to the model, use this exact format:
```python
{
    "role": "tool",
    "tool_call_id": "call_abc123",  # MUST match the id from tool_calls
    "content": "JSON string with the tool result"
}
```

### Common mistakes to avoid

1. **Forgetting `tool_call_id`** — the model will reject tool results without it
2. **Not parsing `arguments`** — they come as a JSON string, not a dict
3. **Not appending the assistant message** — always append `assistant_msg` to
   `messages` before processing tool calls, to maintain conversation history
4. **Raising exceptions in tools** — tools should catch all errors and return
   error strings; never let exceptions propagate
5. **Making the loop async** — `requests.post()` is synchronous; use `def`
   not `async def` unless you switch to `httpx`
6. **No iteration cap** — always limit iterations (10 is a good default)
   to prevent infinite loops if the model keeps requesting tools

### Genie tool null-safety

The Databricks Genie API may return responses where `statement_response` or
`manifest` is `None` — this happens when Genie answers with text instead of
generating a SQL query. Always guard:

```python
if (
    result is None
    or result.statement_response is None
    or result.statement_response.manifest is None
):
    return json.dumps({"genie_text": "No SQL result generated."})
```

## Wiring into FastAPI

In your API router, import and call the agent loop directly:

```python
def _query_agent(user_message: str):
    try:
        from server.agents.agent_loop import run_agent_loop
        response_text = run_agent_loop(user_message)
        return {"agent_response": response_text} if response_text else None
    except Exception as exc:
        logger.warning("Agent loop failed: %s", exc)
        return None
```

No HTTP call to a serving endpoint — the agent runs in-process.
