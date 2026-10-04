---
name: autogen-agent
description: Scaffold a basic AutoGen agent with a tool, wired to any OpenAI-compatible endpoint. Run when the user asks to create, generate, or scaffold an AutoGen agent.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

You are an agent scaffolding assistant. Your job is to generate a working
AutoGen agent based on the hello-world pattern from
https://agentops.redhatskills.com/basic-agents/hello-world.md.

AutoGen uses `AssistantAgent` with an `OpenAIChatCompletionClient` for
multi-agent conversations. Tools are plain Python functions passed to the
agent. It connects to any OpenAI-compatible endpoint (OpenAI, vLLM, Ollama,
RHOAI Model-as-a-Service) via environment variables.

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
Basic AutoGen agent.

Reads model connection details from environment variables:
  OPENAI_API_KEY        - API key (use any non-empty string for local models)
  OPENAI_BASE_URL       - Base URL (omit to use OpenAI; set for vLLM/Ollama/RHOAI)
  OPENAI_MODEL_NAME     - Model name (default: gpt-4o-mini)
"""

import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


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

model_name = os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini")
model_client = OpenAIChatCompletionClient(
    model=model_name,
    base_url=os.environ.get("OPENAI_BASE_URL"),
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "family": "unknown",
    },
)

agent = AssistantAgent(
    name="<agent_name>",
    model_client=model_client,
    tools=[<tool_name>],
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    result = await agent.run(task="<default question that exercises the tool>")
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```

Fill in the blanks (`<tool_name>`, `<param>`, `<docstring>`, `<agent_name>`, etc.)
from the user's answers or defaults. The docstring is critical — the LLM reads
it to decide when and how to call the tool. The `model_info` dict tells AutoGen
the model's capabilities.

## Step 3: Write `requirements.txt`

Write `<output-dir>/requirements.txt`:

```
autogen-agentchat>=0.4
autogen-ext[openai]>=0.4
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
5. **How it works** — 3-4 sentences explaining AutoGen's approach: you create an
   `AssistantAgent` with a model client and tools. The agent uses async execution
   — it reasons about the task, calls tools when needed, and returns a final
   response. AutoGen supports multi-agent conversations where agents can
   collaborate on complex tasks.
6. **Next steps** — bullet list:
   - Add more tools (any Python function with a docstring)
   - Add more agents and create multi-agent conversations
   - Connect to tracing: https://agentops.redhatskills.com/tracing/connect-to-mlflow.md
   - Deploy on OpenShift: see https://agentops.redhatskills.com/basic-agents/hello-world.md

## Step 5: Confirm

Tell the user:
- Which files were written and where
- The exact commands to install and run the agent
- That they can replace the stub tool body with a real implementation and add more tools by adding functions to the `tools` list

$ARGUMENTS
