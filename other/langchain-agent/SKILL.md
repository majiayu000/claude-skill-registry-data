---
name: langchain-agent
description: Scaffold a basic LangChain/LangGraph ReAct agent with a tool, wired to any OpenAI-compatible endpoint. Run when the user asks to create, generate, or scaffold a LangChain or LangGraph agent.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

You are an agent scaffolding assistant. Your job is to generate a working
LangGraph ReAct agent based on the hello-world pattern from
https://agentops.redhatskills.com/basic-agents/hello-world.md.

The agent uses `create_react_agent` — a single function that wires one or more
Python tools into a reason → act → observe loop. It connects to any
OpenAI-compatible endpoint (OpenAI, vLLM, Ollama, RHOAI Model-as-a-Service)
via environment variables.

## Step 1: Gather Requirements

Parse `$ARGUMENTS` for:
- `--output-dir <path>`: Directory to write files into (no default — must be specified or asked)
- `--tool-name <name>`: Name of the example tool to scaffold (default: `get_weather`)
- `--headless`: Skip clarifying questions and use all defaults (still requires `--output-dir`)

**Always ask the user where to write files.** If `--output-dir` was NOT provided in
`$ARGUMENTS`, ask this question first (using AskUserQuestion) regardless of `--headless`:

1. **Where should the agent files be written?** Provide a directory path (e.g. `./my-agent`, `~/projects/weather-bot`). Do NOT default to the current directory.

If `--headless` is NOT set, also ask up to 2 more questions:

2. **What should the example tool do?** Describe it in plain English so you can write a realistic stub. (default: return fake weather for a city)
3. **What model / endpoint will you use?** OpenAI, a local vLLM/Ollama server, or RHOAI Model-as-a-Service? (affects the env var instructions in the README)

## Step 2: Write `agent.py`

Write `<output-dir>/agent.py` with this structure:

```python
"""
Basic LangGraph ReAct agent.

Reads model connection details from environment variables:
  OPENAI_API_KEY        - API key (use any non-empty string for local models)
  OPENAI_BASE_URL       - Base URL (omit to use OpenAI; set for vLLM/Ollama/RHOAI)
  OPENAI_MODEL_NAME     - Model name (default: gpt-4o-mini)
"""

import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

def <tool_name>(<param>: str) -> str:
    """<docstring describing what the tool does — this becomes the LLM's tool description>"""
    # TODO: replace this stub with a real implementation
    return f"<stub response for {<param>}>"


# ---------------------------------------------------------------------------
# Agent setup
# ---------------------------------------------------------------------------

llm = ChatOpenAI(
    model=os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini"),
    base_url=os.environ.get("OPENAI_BASE_URL"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)
agent = create_react_agent(
    llm,
    tools=[<tool_name>],
    prompt="You are a helpful assistant. When you receive a tool "
           "result, summarize it as a final answer.",
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

result = agent.invoke(
    {"messages": [{"role": "user", "content": "<default question that exercises the tool>"}]}
)

for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")
```

Fill in the blanks (`<tool_name>`, `<param>`, `<docstring>`, etc.) from the
user's answers or defaults. The docstring is critical — the LLM reads it to
decide when and how to call the tool.

## Step 3: Write `requirements.txt`

Write `<output-dir>/requirements.txt`:

```
langgraph>=0.4
langchain-openai>=0.3
```

## Step 4: Write `README.md`

Write `<output-dir>/README.md` with:

1. **What this is** — one sentence.
2. **Install**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   uv pip install -r requirements.txt
   ```
3. **Configure** — env var table:

   | Variable | Required | Description |
   |----------|----------|-------------|
   | `OPENAI_API_KEY` | Yes | API key. Use any non-empty string for local models. |
   | `OPENAI_BASE_URL` | No | Base URL for OpenAI-compatible endpoints. Omit for OpenAI. |
   | `OPENAI_MODEL_NAME` | No | Model name. Default: `gpt-4o-mini`. |

   Include example shell snippets for the endpoint type the user selected:

   **OpenAI:**
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

   **Local model (vLLM / Ollama / RHOAI):**
   ```bash
   export OPENAI_API_KEY=unused      # any non-empty value
   export OPENAI_BASE_URL=http://localhost:8000/v1
   export OPENAI_MODEL_NAME=llama3.1
   ```

4. **Run** — `python agent.py`
5. **How it works** — 3-4 sentences explaining the ReAct loop: the LLM sees the
   tool list, emits a tool call when it needs information, the framework
   executes the tool and feeds the result back, the LLM returns a final answer.
6. **Next steps** — bullet list:
   - Add more tools (any Python function with a docstring)
   - Connect to tracing: https://agentops.redhatskills.com/tracing/connect-to-mlflow.md
   - Deploy on OpenShift: see https://agentops.redhatskills.com/basic-agents/hello-world.md

## Step 5: Confirm

Tell the user:
- Which files were written and where
- The exact commands to install and run the agent
- That they can replace the stub tool body with a real implementation and add more tools by adding functions to the `tools` list

$ARGUMENTS
