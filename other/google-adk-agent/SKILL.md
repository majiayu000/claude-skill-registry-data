---
name: google-adk-agent
description: Scaffold a basic Google ADK agent with a tool, wired to any OpenAI-compatible endpoint. Run when the user asks to create, generate, or scaffold a Google ADK agent.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

You are an agent scaffolding assistant. Your job is to generate a working
Google ADK agent based on the hello-world pattern from
https://agentops.redhatskills.com/basic-agents/hello-world.md.

Google ADK uses an `Agent` with a `LiteLlm` model backend, a `Runner` for
execution, and `InMemorySessionService` for session management. Tools are
plain Python functions. It connects to any OpenAI-compatible endpoint
(OpenAI, vLLM, Ollama, RHOAI Model-as-a-Service) via LiteLLM.

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
Basic Google ADK agent.

Reads model connection details from environment variables:
  OPENAI_API_KEY        - API key (use any non-empty string for local models)
  OPENAI_BASE_URL       - Base URL (omit to use OpenAI; set for vLLM/Ollama/RHOAI)
  OPENAI_MODEL_NAME     - Model name (default: gpt-4o-mini)
"""

import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


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

model = LiteLlm(
    model=f"openai/{os.environ.get('OPENAI_MODEL_NAME', 'gpt-4o-mini')}",
    api_base=os.environ.get("OPENAI_BASE_URL"),
    api_key=os.environ.get("OPENAI_API_KEY"),
)

agent = Agent(
    name="<agent_name>",
    model=model,
    description="<one-line description of what this agent does>",
    instruction="<instruction telling the agent when and how to use its tools>",
    tools=[<tool_name>],
)

session_service = InMemorySessionService()
runner = Runner(
    agent=agent, app_name="<app_name>",
    session_service=session_service,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    session = await session_service.create_session(
        app_name="<app_name>", user_id="user1",
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text="<default question that exercises the tool>")],
    )
    async for event in runner.run_async(
        user_id="user1", session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
```

Fill in the blanks (`<tool_name>`, `<param>`, `<docstring>`, `<agent_name>`,
`<app_name>`, etc.) from the user's answers or defaults. The docstring is
critical — the LLM reads it to decide when and how to call the tool.

## Step 3: Write `requirements.txt`

Write `<output-dir>/requirements.txt`:

```
google-adk>=1.2
litellm
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
5. **How it works** — 3-4 sentences explaining Google ADK's approach: you create
   an `Agent` with a model, description, instruction, and tools. A `Runner`
   manages execution with session state via `InMemorySessionService`. The agent
   processes messages asynchronously through `run_async()`, which yields events
   including the final response. ADK uses LiteLLM under the hood to connect to
   any OpenAI-compatible endpoint.
6. **Next steps** — bullet list:
   - Add more tools (any Python function with a docstring)
   - Add sub-agents for multi-agent orchestration
   - Connect to tracing: https://agentops.redhatskills.com/tracing/connect-to-mlflow.md
   - Deploy on OpenShift: see https://agentops.redhatskills.com/basic-agents/hello-world.md

## Step 5: Confirm

Tell the user:
- Which files were written and where
- The exact commands to install and run the agent
- That they can replace the stub tool body with a real implementation and add more tools by adding functions to the `tools` list

$ARGUMENTS
