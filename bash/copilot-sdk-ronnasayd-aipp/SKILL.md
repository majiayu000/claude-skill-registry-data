---
name: copilot-sdk
description: >
  Use this skill whenever the user wants to build Python applications or scripts
  using the GitHub Copilot SDK. Triggers include: building Copilot-powered agents
  or tools in Python, integrating GitHub Copilot CLI programmatically, using the
  copilot Python package, creating sessions with CopilotClient, defining custom
  tools for Copilot, handling streaming from Copilot, setting up custom LLM
  providers (BYOK/Ollama/Azure), permission handling for tool calls, or any
  workflow involving the `copilot` Python package (copilot-sdk). Use this skill
  even if the user only says "Copilot agent", "Copilot session", or "Copilot
  tool" in a Python context — they almost certainly need this.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# GitHub Copilot Python SDK

Python SDK for programmatic control of GitHub Copilot CLI via JSON-RPC.

> **Requirements:** Python 3.11+, GitHub Copilot CLI installed and accessible.

## Installation

```bash
pip install -e ".[telemetry,dev]"
# or
uv pip install -e ".[telemetry,dev]"
```

---

## Core Pattern: CopilotClient + Session

Always prefer async context managers — they handle startup and cleanup automatically.

```python
import asyncio
from copilot import CopilotClient
from copilot.session import PermissionHandler

async def main():
    async with CopilotClient() as client:
        async with await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5",
        ) as session:
            done = asyncio.Event()

            def on_event(event):
                if event.type.value == "assistant.message":
                    print(event.data.content)
                elif event.type.value == "session.idle":
                    done.set()

            session.on(on_event)
            await session.send("Hello!")
            await done.wait()

asyncio.run(main())
```

**Key rule:** `on_permission_request` is **required** in `create_session()` and `resume_session()`. Use `PermissionHandler.approve_all` for dev/trusted environments; write a custom handler for production.

---

## create_session() Parameters

| Parameter               | Type                    | Notes                                                                 |
| ----------------------- | ----------------------- | --------------------------------------------------------------------- |
| `model`                 | str                     | Required with custom providers. e.g. `"gpt-5"`, `"claude-sonnet-4.5"` |
| `on_permission_request` | callable                | **Required.** Sync or async.                                          |
| `on_user_input_request` | callable                | Enables `ask_user` tool                                               |
| `tools`                 | list                    | Custom tool definitions                                               |
| `system_message`        | SystemMessageConfig     | System prompt config                                                  |
| `streaming`             | bool                    | Enable delta streaming events                                         |
| `provider`              | ProviderConfig          | BYOK / custom LLM provider                                            |
| `infinite_sessions`     | InfiniteSessionConfig   | Context compaction config                                             |
| `hooks`                 | SessionHooks            | Lifecycle hook handlers                                               |
| `commands`              | list[CommandDefinition] | Slash commands for TUI                                                |
| `session_id`            | str                     | Custom session ID                                                     |

---

## Defining Custom Tools

### With Pydantic (recommended)

```python
from pydantic import BaseModel, Field
from copilot import define_tool

class SearchParams(BaseModel):
    query: str = Field(description="Search query string")
    limit: int = Field(default=10, description="Max results")

@define_tool(description="Search the internal knowledge base")
async def search_kb(params: SearchParams) -> str:
    results = await db.search(params.query, limit=params.limit)
    return "\n".join(results)

# Pass to create_session:
# tools=[search_kb]
```

**Note:** When using `from __future__ import annotations`, define Pydantic models at module level.

### Override Built-in Tools

```python
@define_tool(name="edit_file", description="Custom editor", overrides_built_in_tool=True)
async def edit_file(params: EditFileParams) -> str: ...
```

### Skip Permission Prompt

```python
@define_tool(name="safe_read", description="Read-only lookup", skip_permission=True)
async def safe_read(params: ReadParams) -> str: ...
```

---

## Permission Handling

```python
from copilot.session import PermissionRequestResult
from copilot.generated.session_events import PermissionRequest

def on_permission_request(request: PermissionRequest, invocation: dict) -> PermissionRequestResult:
    # request.kind.value: "shell" | "write" | "read" | "mcp" | "custom-tool" | "url" | "memory" | "hook"
    # request.tool_name, request.file_name, request.full_command_text
    if request.kind.value == "shell":
        return PermissionRequestResult(kind="denied-interactively-by-user")
    return PermissionRequestResult(kind="approved")
```

Permission result kinds: `"approved"`, `"denied-interactively-by-user"`, `"denied-by-rules"`, `"denied-by-content-exclusion-policy"`, `"no-result"`.

---

## Streaming

```python
async with await client.create_session(
    on_permission_request=PermissionHandler.approve_all,
    model="gpt-5",
    streaming=True,
) as session:
    done = asyncio.Event()

    def on_event(event):
        match event.type.value:
            case "assistant.message_delta":
                print(event.data.delta_content or "", end="", flush=True)
            case "assistant.message":
                print()  # newline after streaming ends
            case "session.idle":
                done.set()

    session.on(on_event)
    await session.send("Tell me a story")
    await done.wait()
```

---

## Custom Providers (BYOK)

When using a custom provider, `model` is **required**.

```python
# Ollama (local)
provider={"type": "openai", "base_url": "http://localhost:11434/v1"}

# Custom OpenAI-compatible
provider={"type": "openai", "base_url": "https://my-api.example.com/v1", "api_key": os.environ["MY_KEY"]}

# Azure OpenAI — MUST use type "azure", NOT "openai"
provider={
    "type": "azure",
    "base_url": "https://my-resource.openai.azure.com",  # host only, no path
    "api_key": os.environ["AZURE_KEY"],
    "azure": {"api_version": "2024-10-21"},
}
```

> **Azure pitfall:** Use `"type": "azure"` for `*.openai.azure.com` endpoints. Using `"openai"` will fail.

---

## Session Hooks

```python
async def on_pre_tool_use(input, invocation):
    # input["toolName"], input["toolArgs"]
    return {"permissionDecision": "allow", "modifiedArgs": input.get("toolArgs")}

async def on_error_occurred(input, invocation):
    # input["error"], input["errorContext"]
    return {"errorHandling": "retry"}  # "retry" | "skip" | "abort"

# In create_session:
hooks={
    "on_pre_tool_use": on_pre_tool_use,
    "on_post_tool_use": ...,
    "on_user_prompt_submitted": ...,
    "on_session_start": ...,
    "on_session_end": ...,
    "on_error_occurred": on_error_occurred,
}
```

---

## Image Attachments

```python
# From file path
await session.send("Describe this image", attachments=[{"type": "file", "path": "/path/to/image.jpg"}])

# From base64
await session.send("Describe this", attachments=[{"type": "blob", "data": b64_data, "mimeType": "image/png"}])
```

---

## Infinite Sessions (Context Compaction)

```python
# Default: enabled. Customize thresholds:
infinite_sessions={
    "enabled": True,
    "background_compaction_threshold": 0.80,
    "buffer_exhaustion_threshold": 0.95,
}

# Disable:
infinite_sessions={"enabled": False}
```

Emits `session.compaction_start` and `session.compaction_complete` events.

---

## UI Elicitation

Only available when `session.capabilities["ui"]["elicitation"]` is truthy.

```python
ui_caps = session.capabilities.get("ui", {})
if ui_caps.get("elicitation"):
    ok = await session.ui.confirm("Deploy to production?")
    env = await session.ui.select("Choose env:", ["staging", "production"])
    name = await session.ui.input("Enter name:", {"format": "email"})
```

---

## Telemetry (OpenTelemetry)

```python
from copilot import CopilotClient, SubprocessConfig

client = CopilotClient(SubprocessConfig(
    telemetry={"otlp_endpoint": "http://localhost:4318"}
))
```

Install extras: `pip install copilot-sdk[telemetry]`

---

## Manual Lifecycle Management

Use only when you need fine-grained control:

```python
client = CopilotClient()
await client.start()
session = await client.create_session(on_permission_request=PermissionHandler.approve_all, model="gpt-5")
# ... use session ...
await session.disconnect()
await client.stop()
```

---

## SubprocessConfig Options

```python
from copilot import CopilotClient, SubprocessConfig

client = CopilotClient(SubprocessConfig(
    cli_path=None,            # path to CLI binary or COPILOT_CLI_PATH env var
    github_token="ghp_...",   # takes priority over other auth methods
    use_stdio=True,           # stdio vs TCP transport
    log_level="info",
    env={"MY_VAR": "value"},
))
```

---

## Common Event Types

| Event                               | When                                               |
| ----------------------------------- | -------------------------------------------------- |
| `assistant.message`                 | Full response ready                                |
| `assistant.message_delta`           | Streaming chunk (requires `streaming=True`)        |
| `assistant.reasoning` / `_delta`    | Chain-of-thought (model-dependent)                 |
| `session.idle`                      | Session done processing — use to signal completion |
| `session.compaction_start/complete` | Context compaction lifecycle                       |
| `session.created/deleted/updated`   | Lifecycle (client-level)                           |

---

For detailed API reference, see the full README:
https://github.com/github/copilot-sdk/blob/main/python/README.md
